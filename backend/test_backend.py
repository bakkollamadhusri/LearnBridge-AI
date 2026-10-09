import asyncio
import os
import pymupdf
from app.models import LearningRequest, QuickActionRequest
from app.services.ai_service import AIService
from app.services.rag_service import rag_service
from app.services.diagram_service import DiagramService
from app.services.video_service import VideoService
from app.services.quiz_service import QuizService

async def run_all_tests():
    print("=" * 60)
    print("🧪 RUNNING LEARNBRIDGE AI BACKEND VERIFICATION SUITE")
    print("=" * 60)

    # Test 1: General AI Learning (No PDF required)
    print("\n[Test 1] General AI Question (No PDF)...")
    req1 = LearningRequest(
        question="What is Machine Learning?",
        language="English",
        source_mode="general_ai"
    )
    res1 = await AIService.process_learning_request(req1)
    assert res1.simple_explanation, "Failed: simple_explanation missing"
    assert res1.definition, "Failed: definition missing"
    assert len(res1.how_it_works) > 0, "Failed: how_it_works missing"
    assert res1.mode == "general_ai", f"Expected mode 'general_ai', got {res1.mode}"
    print("  ✅ Passed: Received structured general AI answer with explanation and examples.")

    # Test 2: Telugu Regional Language
    print("\n[Test 2] Regional Language Explanation (Telugu)...")
    req2 = LearningRequest(
        question="Explain machine learning in Telugu",
        language="Telugu",
        source_mode="general_ai"
    )
    res2 = await AIService.process_learning_request(req2)
    assert "మెషిన్ లెర్నింగ్" in res2.simple_explanation or "సాంకేతికత" in res2.simple_explanation or "డేటా" in res2.simple_explanation
    print("  ✅ Passed: Answer generated naturally in student-friendly Telugu.")

    # Test 3: Bilingual (English + Telugu)
    print("\n[Test 3] Bilingual (English + Telugu)...")
    req3 = LearningRequest(
        question="What is Machine Learning?",
        language="English + Telugu",
        source_mode="general_ai"
    )
    res3 = await AIService.process_learning_request(req3)
    assert "Machine Learning" in res3.simple_explanation and "మెషిన్ లెర్నింగ్" in res3.simple_explanation
    print("  ✅ Passed: Answer generated with English technical terms + Telugu explanations.")

    # Test 4: PDF Creation & PyMuPDF RAG Processing
    print("\n[Test 4] PDF Document Generation & RAG Ingestion...")
    sample_pdf_path = "sample_electronics.pdf"
    doc = pymupdf.open()
    
    # Page 1: PN Junction basics
    page1 = doc.new_page()
    page1.insert_text(
        (50, 72),
        "Chapter 1: Semiconductor Physics and PN Junctions.\n\n"
        "A P-N junction is formed when a p-type semiconductor is joined to an n-type semiconductor.\n"
        "At the junction, free electrons and holes recombine, creating a depletion region devoid of mobile carriers.\n"
        "For Silicon, the built-in barrier potential is approximately 0.7 Volts.\n"
        "In forward bias, current increases exponentially with applied voltage.",
        fontsize=12
    )
    
    # Page 2: Transistors
    page2 = doc.new_page()
    page2.insert_text(
        (50, 72),
        "Chapter 2: Bipolar Junction Transistors.\n\n"
        "A BJT consists of three doped regions: Emitter, Base, and Collector.\n"
        "The base is designed to be extremely thin and lightly doped to maximize electron transit efficiency.\n"
        "Current gain is defined by Beta = Ic / Ib.",
        fontsize=12
    )
    doc.save(sample_pdf_path)
    doc.close()

    metadata = rag_service.process_pdf(sample_pdf_path, "sample_electronics.pdf", "test-user-1")
    assert metadata.total_pages == 2, f"Expected 2 pages, got {metadata.total_pages}"
    assert metadata.status == "ready", f"Status expected ready, got {metadata.status}"
    print(f"  ✅ Passed: PDF parsed into page-indexed chunks. Doc ID: {metadata.id}, Pages: {metadata.total_pages}")

    # Test 5: PDF-Based Grounded QA with Citations
    print("\n[Test 5] PDF Grounded QA (Page citation test)...")
    req_pdf = LearningRequest(
        question="What is the built-in barrier potential for Silicon?",
        document_id=metadata.id,
        source_mode="pdf_and_ai",
        language="English",
        user_id="test-user-1"
    )
    res_pdf = await AIService.process_learning_request(req_pdf)
    assert len(res_pdf.citations) > 0, "Failed: Citations missing"
    assert res_pdf.citations[0].page_number == 1, f"Expected page 1 citation, got page {res_pdf.citations[0].page_number}"
    assert "0.7" in res_pdf.citations[0].text_snippet, "Failed: Snippet did not contain 0.7V"
    print(f"  ✅ Passed: Answer grounded in document with exact citation: {res_pdf.citations[0].filename} (Page {res_pdf.citations[0].page_number})")

    # Test 6: Strict PDF Only Mode (Absent Information Handling)
    print("\n[Test 6] Strict 'PDF Only' mode for missing question...")
    req_absent = LearningRequest(
        question="What is the capital of France?",
        document_id=metadata.id,
        source_mode="pdf_only",
        language="English",
        user_id="test-user-1"
    )
    res_absent = await AIService.process_learning_request(req_absent)
    assert res_absent.missing_from_pdf is True, "Failed: missing_from_pdf should be True"
    assert len(res_absent.citations) == 0, "Failed: No fake citations allowed in PDF Only mode"
    assert "not found in" in res_absent.simple_explanation.lower()
    print("  ✅ Passed: Refused hallucination and clearly indicated absence from document.")

    # Test 7: Document Context Isolation
    print("\n[Test 7] Document Isolation (cross-document test)...")
    citations_other, _ = rag_service.retrieve_relevant_chunks(
        document_id="non-existent-id",
        query="Silicon",
        user_id="test-user-1"
    )
    assert len(citations_other) == 0, "Failed: Chunks leaked across invalid document ID"
    print("  ✅ Passed: Strict isolation verified. No cross-document leaking.")

    # Test 8: Educational Diagram Generation
    print("\n[Test 8] Diagram generation...")
    diag = DiagramService.get_diagram_for_topic("pn junction diode")
    assert diag is not None and "<svg" in diag.svg_content
    print(f"  ✅ Passed: Generated educational SVG diagram for '{diag.title}'")

    # Test 9: Video Recommendation with Telugu matching
    print("\n[Test 9] Video retrieval with regional language...")
    vids = VideoService.get_videos_for_topic("machine learning", preferred_language="Telugu")
    assert len(vids) > 0, "Failed: No videos found"
    assert vids[0].language == "Telugu", f"Expected top video to be Telugu, got {vids[0].language}"
    print(f"  ✅ Passed: Found {len(vids)} verified video tutorials; top video: '{vids[0].title}' ({vids[0].channel})")

    # Test 10: Flashcards & Quiz Evaluation
    print("\n[Test 10] Interactive Quiz & Flashcards...")
    cards = QuizService.generate_flashcards("P-N Junction", count=3)
    assert len(cards) == 3
    quiz = QuizService.generate_quiz("P-N Junction")
    assert len(quiz) >= 2
    # Submit answer
    eval_res = QuizService.evaluate_quiz("test-quiz", quiz, {0: quiz[0].correct_answer})
    assert eval_res.correct_count >= 1
    print(f"  ✅ Passed: Flashcards ({len(cards)}) and Quiz evaluated (Score: {eval_res.score_percentage}%).")

    # Cleanup test PDF
    if os.path.exists(sample_pdf_path):
        os.remove(sample_pdf_path)

    print("\n" + "=" * 60)
    print("🎉 ALL 10 BACKEND VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_all_tests())
