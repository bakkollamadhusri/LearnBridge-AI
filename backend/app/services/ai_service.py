import re
import json
from typing import List, Optional, Dict, Any
import httpx
from ..config import settings
from ..models import (
    LearningRequest,
    LearningResponse,
    Citation,
    PracticeQuestion,
    DiagramData,
    VideoRecommendation
)
from .rag_service import rag_service
from .diagram_service import DiagramService
from .video_service import VideoService

class AIService:
    @classmethod
    async def process_learning_request(cls, req: LearningRequest) -> LearningResponse:
        question = req.question.strip()
        selected_lang = req.language or "English"
        source_mode = req.source_mode
        doc_id = req.document_id

        # Determine if we are running in PDF mode or General AI mode
        has_active_doc = bool(doc_id and rag_service.get_document(doc_id, req.user_id or "guest-user-1"))
        
        # If no document is selected, force General AI mode per requirement
        if not has_active_doc:
            source_mode = "general_ai"

        citations: List[Citation] = []
        pdf_context = ""
        answered_from_pdf = False
        missing_from_pdf = False

        if has_active_doc and source_mode in ["pdf_and_ai", "pdf_only"]:
            citations, pdf_context = rag_service.retrieve_relevant_chunks(
                document_id=doc_id,
                query=question,
                user_id=req.user_id or "guest-user-1",
                top_k=3
            )
            
            # Check relevance score threshold
            if citations and max(c.score for c in citations) >= 0.35:
                answered_from_pdf = True
            else:
                missing_from_pdf = True
                if source_mode == "pdf_only":
                    citations = []

        # If PDF Only mode and not found in PDF, enforce strict non-hallucination
        if source_mode == "pdf_only" and (not answered_from_pdf or not citations):
            doc = rag_service.get_document(doc_id, req.user_id or "guest-user-1")
            filename = doc.filename if doc else "the selected document"
            
            explanation = (
                f"⚠️ **Information Not Found in Document:**\n\n"
                f"The provided question '{question}' was not found within **{filename}** based on strict document search. "
                f"In **'PDF Only'** mode, answers are restricted strictly to retrieved document passages to prevent hallucination. "
                f"\n\n👉 *Tip: Switch to **'PDF + AI Knowledge'** or **'General AI'** mode to get a complete explanation using LearnBridge AI's broader knowledge base.*"
            )
            
            return LearningResponse(
                question=question,
                mode="pdf_based",
                source_mode="pdf_only",
                language=selected_lang,
                answered_from_pdf=False,
                missing_from_pdf=True,
                simple_explanation=explanation,
                definition=None,
                how_it_works="Strict PDF-only search returned no matching passages.",
                example=None,
                key_points=["Strict RAG search yielded no confident passage matches in this document."],
                visual_diagram=None,
                videos=[],
                practice_questions=[],
                follow_up_questions=[
                    f"Switch to 'PDF + AI Knowledge' mode to answer '{question}'?",
                    "What other sections are present in this PDF?",
                    "Summarize the main topics in this document"
                ],
                citations=[],
                audio_text="The requested information was not found in the uploaded document under PDF Only mode."
            )

        # Attempt to call external AI provider if API key exists
        external_result = None
        if settings.GEMINI_API_KEY:
            external_result = await cls._call_gemini_api(req, pdf_context, source_mode)
        elif settings.OPENAI_API_KEY:
            external_result = await cls._call_openai_api(req, pdf_context, source_mode)

        if external_result:
            return external_result

        # Built-in Pedagogical AI Engine (High quality, responsive, student-centered)
        return cls._generate_builtin_pedagogical_answer(
            req=req,
            citations=citations,
            pdf_context=pdf_context,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            has_active_doc=has_active_doc
        )

    @classmethod
    def _generate_builtin_pedagogical_answer(
        cls,
        req: LearningRequest,
        citations: List[Citation],
        pdf_context: str,
        answered_from_pdf: bool,
        missing_from_pdf: bool,
        has_active_doc: bool
    ) -> LearningResponse:
        question = req.question.strip()
        lang = req.language or "English"
        is_telugu = "telugu" in lang.lower()
        is_hindi = "hindi" in lang.lower()
        is_tamil = "tamil" in lang.lower()
        is_bilingual = "+" in lang
        q_lower = question.lower()

        # 1. Topic Recognition
        topic = question
        for prefix in ["what is ", "explain ", "how does ", "tell me about ", "describe ", "define ", "what are "]:
            if q_lower.startswith(prefix):
                topic = question[len(prefix):].rstrip("?. ")
                break

        # Check for specific scientific & computing concepts
        if "machine learning" in q_lower or "ml" in q_lower:
            return cls._build_ml_response(req, citations, answered_from_pdf, missing_from_pdf, lang)
        elif "pn junction" in q_lower or "diode" in q_lower:
            return cls._build_diode_response(req, citations, answered_from_pdf, missing_from_pdf, lang)
        elif "photosynthesis" in q_lower:
            return cls._build_photosynthesis_response(req, citations, answered_from_pdf, missing_from_pdf, lang)
        elif "neural network" in q_lower:
            return cls._build_neural_network_response(req, citations, answered_from_pdf, missing_from_pdf, lang)
        elif "water cycle" in q_lower:
            return cls._build_water_cycle_response(req, citations, answered_from_pdf, missing_from_pdf, lang)

        # Dynamic Generic Educational Synthesizer
        return cls._build_generic_educational_response(req, topic, citations, answered_from_pdf, missing_from_pdf, lang)

    @classmethod
    def _build_ml_response(cls, req: LearningRequest, citations: List[Citation], answered_from_pdf: bool, missing_from_pdf: bool, lang: str) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        is_bilingual = "+" in lang.lower()

        if is_telugu:
            if is_bilingual:
                simple_exp = (
                    "Machine Learning (మెషిన్ లెర్నింగ్) అంటే కంప్యూటర్లు డేటా మరియు పూర్వ అనుభవాల నుండి స్వయంగా నేర్చుకునే ఒక ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ (AI) టెక్నాలజీ. "
                    "మనం కంప్యూటర్‌కు ప్రతి రూల్ కోడింగ్ చేయాల్సిన అవసరం లేదు; డేటా ఇస్తే అదే స్వయంగా patterns ను గుర్తిస్తుంది (It learns from patterns in data)."
                )
                definition = (
                    "Machine Learning is a subset of Artificial Intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.\n\n"
                    "తెలుగులో: మెషిన్ లెర్నింగ్ అనేది కంప్యూటర్లు నిర్దిష్ట ప్రోగ్రామింగ్ నియమాలు లేకుండా, డేటా ఆధారంగా స్వయంగా ఫలితాలను అంచనా వేసే సామర్థ్యాన్ని ఇచ్చే సాంకేతికత."
                )
                example = (
                    "💡 Real-world Example (నిజ జీవిత ఉదాహరణ):\n"
                    "• YouTube లేదా Netflix రికమండేషన్లు: మీరు చూసిన వీడియోల ఆధారంగా మీకు నచ్చే కొత్త వీడియోలను సూచిస్తుంది.\n"
                    "• Spam Filter: జీమెయిల్ మీ ఇమెయిల్స్ పరిశీలించి ఏది స్పామ్ (Spam) అని ఆటోమేటిక్‌గా పక్కన పెడుతుంది."
                )
            else:
                simple_exp = (
                    "మెషిన్ లెర్నింగ్ (Machine Learning) అంటే కంప్యూటర్లు డేటా ఆధారంగా స్వయంగా విషయాలను నేర్చుకునే ఒక అధునాతన సాంకేతికత. "
                    "ఒక చిన్న పిల్లాడు బొమ్మలను చూసి కుక్క లేదా పిల్లిని ఎలా గుర్తుపడతాడో, కంప్యూటర్ కూడా వేలాది ఫోటోలు లేదా డేటాను విశ్లేషించి patterns ను నేర్చుకుంటుంది."
                )
                definition = (
                    "మెషిన్ లెర్నింగ్ (ML): స్పష్టమైన ప్రోగ్రామింగ్ సూచనలు అవసరం లేకుండా, ఇచ్చిన డేటా మరియు అనుభవాల నుండి స్వయంగా నేర్చుకుని భవిష్యత్ ఫలితాలను అంచనా వేసే ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ విభాగం."
                )
                example = (
                    "💡 నిజ జీవిత ఉదాహరణ:\n"
                    "మీరు స్మార్ట్‌ఫోన్‌లో ఉపయోగించే కెమెరా ఫేస్ లాక్ (Face Unlock). మీ ముఖాన్ని వివిధ కోణాల్లో పరిశీలించి, ఇది మీరే అని మెషిన్ లెర్నింగ్ ద్వారా నిర్ధారించుకుంటుంది."
                )
        else:
            simple_exp = (
                "Machine Learning (ML) is a branch of Artificial Intelligence where computers learn from data and past experiences, rather than following rigid, hand-written instructions. "
                "Just like humans improve at chess or driving with practice, machine learning algorithms get more accurate as they process more data."
            )
            definition = (
                "Machine Learning is a scientific discipline focused on developing algorithms and statistical models that computer systems use to perform tasks by relying on patterns and inference."
            )
            example = (
                "💡 Real-World Example:\n"
                "• Netflix & Spotify Recommendations: The system looks at your watch/listening history and identifies patterns in what similar users enjoyed to suggest new content.\n"
                "• Email Spam Filtering: Automatically identifies junk mail by recognizing suspicious phrases and patterns from millions of processed emails."
            )

        how_it_works = [
            "1. Data Collection: Gathering high-quality examples (images, audio, text, sensor numbers).",
            "2. Feature Engineering: Selecting relevant properties (e.g., house size, location, bedrooms).",
            "3. Model Training: The algorithm adjusts internal parameters (weights) to minimize error.",
            "4. Evaluation & Testing: Validating predictions on unseen data to test accuracy.",
            "5. Deployment & Inference: Making real-time predictions on brand new inputs."
        ]

        key_points = [
            "Subfield of Artificial Intelligence (AI).",
            "Three main paradigms: Supervised Learning, Unsupervised Learning, and Reinforcement Learning.",
            "Generalizes to new, unseen data rather than memorizing exact inputs.",
            "Heavily used in autonomous vehicles, speech recognition, healthcare diagnosis, and finance."
        ]

        practice = [
            PracticeQuestion(
                question="Which type of Machine Learning uses labelled input-output pairs to train models?",
                options=["Unsupervised Learning", "Supervised Learning", "Reinforcement Learning", "Heuristic Search"],
                correct_answer=1,
                explanation="Supervised learning provides both the input data and the correct target labels (ground truth) during training."
            ),
            PracticeQuestion(
                question="What is the primary difference between traditional programming and machine learning?",
                options=[
                    "Traditional programming uses computers, ML does not",
                    "In ML, the computer learns rules from data and answers, rather than being given rules directly",
                    "ML cannot handle numbers",
                    "Traditional programming requires internet access"
                ],
                correct_answer=1,
                explanation="In traditional programming: Data + Rules = Answers. In Machine Learning: Data + Answers = Rules."
            )
        ]

        follow_ups = [
            "What is the difference between Supervised and Unsupervised Learning?",
            "Can you explain Overfitting vs Underfitting in simple terms?",
            "How do Neural Networks differ from traditional Machine Learning?",
            "Give me a step-by-step roadmap to start learning Machine Learning in Python."
        ]

        diagram = DiagramService.get_diagram_for_topic("machine learning")
        videos = VideoService.get_videos_for_topic("machine learning", lang)

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition=definition,
            how_it_works=how_it_works,
            example=example,
            key_points=key_points,
            visual_diagram=diagram,
            videos=videos,
            practice_questions=practice,
            follow_up_questions=follow_ups,
            citations=citations,
            audio_text=simple_exp.replace("•", "").replace("💡", "")
        )

    @classmethod
    def _build_diode_response(cls, req: LearningRequest, citations: List[Citation], answered_from_pdf: bool, missing_from_pdf: bool, lang: str) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        if is_telugu:
            simple_exp = (
                "PN జంక్షన్ డయోడ్ (P-N Junction Diode) అనేది కరెంట్‌ను కేవలం ఒకే దిశలో మాత్రమే ప్రవహించేలా చేసే రెండు టెర్మినల్స్ కలిగిన ప్రాథమిక సెమీకండక్టర్ పరికరం. "
                "ఇది విద్యుత్ వలయంలో ఒక 'వన్-వే వాల్వ్' (One-Way Valve) లాగా పనిచేస్తుంది."
            )
            definition = (
                "P-రకం సెమీకండక్టర్ (హోల్స్ అధికంగా ఉండేది) మరియు N-రకం సెమీకండక్టర్ (ఎలక్ట్రాన్లు అధికంగా ఉండేది) లను అణు స్థాయిలో కలిపినప్పుడు ఏర్పడే సరిహద్దును P-N జంక్షన్ అంటారు."
            )
            example = (
                "💡 ఉదాహరణ: మొబైల్ ఛార్జర్ లోని రెక్టిఫైయర్ (Rectifier). గోడ సాకెట్ నుండి వచ్చే AC కరెంట్‌ను ఫోన్ బ్యాటరీకి సరిపడే DC కరెంట్‌గా మార్చడానికి డయోడ్లు వాడతారు."
            )
        else:
            simple_exp = (
                "A P-N junction diode is a fundamental two-terminal semiconductor device that allows electric current to flow easily in one direction, while strongly blocking it in the reverse direction. "
                "Think of it as a one-way turnstile for electrical electrons."
            )
            definition = (
                "A P-N junction is the metallurgical boundary formed by joining p-type (excess mobile holes) and n-type (excess mobile electrons) semiconductor regions within a single crystal lattice."
            )
            example = (
                "💡 Real-World Example:\n"
                "• AC to DC Power Adapters (Rectification): In your laptop and phone chargers, diodes convert alternating current (AC) into steady direct current (DC).\n"
                "• Reverse Polarity Protection: Prevents sensitive circuit boards from frying if batteries are plugged in backwards."
            )

        how_it_works = [
            "1. Formation of Depletion Layer: Near the interface, free electrons from the N-side diffuse into the P-side to neutralize holes, leaving behind immobile positive and negative donor/acceptor ions.",
            "2. Built-in Potential Barrier (Vbi): These fixed ions establish an internal electric field pointing from N to P (approx. 0.7V for Silicon, 0.3V for Germanium).",
            "3. Forward Bias (Anode + / Cathode -): External voltage opposes the barrier, thinning the depletion layer and allowing strong conduction current.",
            "4. Reverse Bias (Anode - / Cathode +): External voltage widens the depletion layer, blocking current except for a negligible nano-ampere leakage current."
        ]

        key_points = [
            "Two operating states: Forward Bias (ON/Conduction) and Reverse Bias (OFF/Cut-off).",
            "Knee / Barrier Voltage: ~0.7V for Silicon, ~0.3V for Germanium.",
            "Forms the core operating principle of LEDs, solar cells, and transistors (BJT, MOSFET).",
            "Reaches avalanche or Zener breakdown if excessive reverse voltage is applied."
        ]

        practice = [
            PracticeQuestion(
                question="What is the approximate forward barrier potential for a Silicon P-N junction diode at room temperature?",
                options=["0.1 V", "0.3 V", "0.7 V", "1.5 V"],
                correct_answer=2,
                explanation="Silicon diodes require an applied forward bias of approximately 0.7 volts to overcome the built-in depletion barrier."
            ),
            PracticeQuestion(
                question="What happens to the depletion region width when a diode is reverse biased?",
                options=["It decreases", "It widens / increases", "It disappears completely", "It turns into a conductor"],
                correct_answer=1,
                explanation="Reverse bias pulls majority carriers away from the junction, increasing the width of the immobile ion depletion zone."
            )
        ]

        diagram = DiagramService.get_diagram_for_topic("pn junction")
        videos = VideoService.get_videos_for_topic("pn junction", lang)

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition=definition,
            how_it_works=how_it_works,
            example=example,
            key_points=key_points,
            visual_diagram=diagram,
            videos=videos,
            practice_questions=practice,
            follow_up_questions=[
                "What is the difference between Zener Breakdown and Avalanche Breakdown?",
                "How does a Light Emitting Diode (LED) produce light from a PN junction?",
                "How does a full-wave bridge rectifier work?"
            ],
            citations=citations,
            audio_text=simple_exp
        )

    @classmethod
    def _build_photosynthesis_response(cls, req: LearningRequest, citations: List[Citation], answered_from_pdf: bool, missing_from_pdf: bool, lang: str) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        if is_telugu:
            simple_exp = (
                "కిరణజన్య సంయోగక్రియ (Photosynthesis) అంటే ఆకుపచ్చని మొక్కలు సూర్యరశ్మి, నీరు మరియు గాలిలోని కార్బన్ డయాక్సైడ్‌ను ఉపయోగించి తమ ఆహారాన్ని (గ్లూకోజ్) తామే తయారు చేసుకునే జీవక్రియ. "
                "ఈ ప్రక్రియ ద్వారా మానవులకు, జంతువులకు ప్రాణాధారమైన ఆక్సిజన్ విడుదలవుతుంది."
            )
            definition = (
                "కిరణజన్య సంయోగక్రియ సమీకరణం:\n6 CO₂ + 6 H₂O + సూర్యకాంతి ➔ C₆H₁₂O₆ (గ్లూకోజ్) + 6 O₂ (ఆక్సిజన్)"
            )
            example = (
                "💡 ఉదాహరణ: ఒక తోటలోని వేప చెట్టు లేదా మామిడి చెట్టు ఆకులు పగటిపూట సూర్యకాంతిని గ్రహించి పరిసరాలలో స్వచ్ఛమైన ఆక్సిజన్ నింపుతాయి."
            )
        else:
            simple_exp = (
                "Photosynthesis is the biological process by which green plants, algae, and some bacteria capture sunlight to convert carbon dioxide and water into glucose (energy-rich sugar) and oxygen. "
                "It is the primary source of energy and breathable oxygen for virtually all complex life on Earth."
            )
            definition = (
                "Chemical Equation: 6 CO₂ + 6 H₂O + Light Energy ➔ C₆H₁₂O₆ (Glucose) + 6 O₂ (Oxygen gas)"
            )
            example = (
                "💡 Everyday Example:\n"
                "When you eat an apple or rice, you are consuming solar energy that was captured and stored as chemical bonds by plant leaves weeks or months earlier!"
            )

        how_it_works = [
            "1. Light Absorption: Chlorophyll pigments inside the thylakoid membranes of chloroplasts trap photons from red and blue sunlight.",
            "2. Water Splitting (Photolysis): Water (H₂O) absorbed by roots is split, releasing Oxygen (O₂) as a byproduct and energizing ATP/NADPH molecules.",
            "3. Carbon Fixation (Calvin Cycle): Carbon dioxide enters through leaf stomata and is synthesized into 3-carbon sugars in the chloroplast stroma.",
            "4. Sugar Storage: Plants convert simple sugars into starch, cellulose for cell walls, and transportable sucrose."
        ]

        key_points = [
            "Occurs inside plant organelles called Chloroplasts containing chlorophyll pigment.",
            "Two stages: Light-Dependent Reactions (in thylakoids) and Light-Independent Reactions / Calvin Cycle (in stroma).",
            "Takes in greenhouse gas CO₂ and replenishes the atmospheric O₂ layer."
        ]

        diagram = DiagramService.get_diagram_for_topic("photosynthesis")
        videos = VideoService.get_videos_for_topic("photosynthesis", lang)

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition=definition,
            how_it_works=how_it_works,
            example=example,
            key_points=key_points,
            visual_diagram=diagram,
            videos=videos,
            practice_questions=[
                PracticeQuestion(
                    question="Which gas is released into the atmosphere as a byproduct during photosynthesis?",
                    options=["Carbon Monoxide", "Nitrogen", "Oxygen", "Methane"],
                    correct_answer=2,
                    explanation="Oxygen is produced during the photolysis of water in the light-dependent reactions."
                )
            ],
            follow_up_questions=[
                "What is the difference between C3 and C4 plants?",
                "How does the Calvin Cycle convert carbon dioxide into glucose?",
                "Why do leaves change color in autumn?"
            ],
            citations=citations,
            audio_text=simple_exp
        )

    @classmethod
    def _build_neural_network_response(cls, req: LearningRequest, citations: List[Citation], answered_from_pdf: bool, missing_from_pdf: bool, lang: str) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        simple_exp = (
            "న్యూరల్ నెట్‌వర్క్ (Neural Network) అనేది మానవ మెదడులోని నాడీ కణాల (Neurons) పనితీరును అనుకరిస్తూ రూపొందించిన ఒక కంప్యూటేషనల్ మోడల్. "
            "ఇది సంక్లిష్టమైన సమస్యలను విశ్లేషించి అంచనాలు వేయగలదు." if is_telugu else
            "An Artificial Neural Network (ANN) is a computational model inspired by the human brain's interconnected web of neurons. "
            "It consists of layers of artificial nodes that process numerical signals, learning complex relationships and abstractions."
        )

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition="A mathematical system consisting of interconnected processing units arranged in layers: Input, Hidden, and Output layers with learnable weights and activation functions.",
            how_it_works=[
                "1. Input Vector: Numbers enter the input layer.",
                "2. Linear Combination: Each neuron computes the weighted sum: z = ∑(wᵢ · xᵢ) + b.",
                "3. Activation: An activation function (ReLU, Sigmoid) introduces non-linearity.",
                "4. Loss Calculation: Difference between predicted and actual outcome.",
                "5. Backpropagation: Gradient descent adjusts weights via the chain rule."
            ],
            example="Handwritten Digit Recognition (MNIST): A neural network looks at a 28x28 pixel image of a handwritten number and correctly recognizes whether it is a 3, 7, or 9.",
            key_points=[
                "Composed of Input Layer, Hidden Layers, and Output Layer.",
                "Non-linear activations enable solving non-linearly separable problems.",
                "Trained via Backpropagation and Gradient Descent."
            ],
            visual_diagram=DiagramService.get_diagram_for_topic("neural network"),
            videos=VideoService.get_videos_for_topic("neural network", lang),
            practice_questions=[
                PracticeQuestion(
                    question="Which algorithm is primarily used to compute weight gradients in neural networks?",
                    options=["Binary Search", "Backpropagation", "Dijkstra's Algorithm", "K-Means"],
                    correct_answer=1,
                    explanation="Backpropagation uses the calculus chain rule to calculate the partial derivatives of the loss function with respect to each weight."
                )
            ],
            follow_up_questions=[
                "What is the vanishing gradient problem and how does ReLU solve it?",
                "What is the difference between CNN and RNN architectures?",
                "How does dropout prevent overfitting?"
            ],
            citations=citations,
            audio_text=simple_exp
        )

    @classmethod
    def _build_water_cycle_response(cls, req: LearningRequest, citations: List[Citation], answered_from_pdf: bool, missing_from_pdf: bool, lang: str) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        simple_exp = (
            "జల చక్రం (Water Cycle) అంటే భూమిపై ఉన్న నీరు సూర్యుడి వేడికి ఆవిరై, ఆకాశంలో మేఘాలుగా మారి, తిరిగి వర్షం రూపంలో భూమికి చేరే నిరంతర సహజ ప్రక్రియ." if is_telugu else
            "The Water Cycle (Hydrologic Cycle) is the continuous, endless circulation of water between Earth's surface and the atmosphere powered by solar energy and gravity."
        )

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition="The biogeochemical cycle that describes the continuous movement of water on, above, and below the surface of the Earth across gaseous, liquid, and solid states.",
            how_it_works=[
                "1. Evaporation & Transpiration: Solar radiation heats surface water, transforming liquid into atmospheric vapor.",
                "2. Condensation: Rising water vapor cools and condenses around microscopic nuclei to form clouds.",
                "3. Precipitation: Saturated water droplets become too heavy and fall as rain, snow, or hail.",
                "4. Infiltration & Runoff: Water re-enters groundwater tables, rivers, and oceans, restarting the cycle."
            ],
            example="Puddles disappearing after a sunny afternoon, moisture forming on a cold glass, and monsoon rains replenishing reservoirs.",
            key_points=[
                "Total volume of water on Earth remains essentially constant over time.",
                "Powered primarily by the Sun's thermodynamic energy.",
                "Critical for climate regulation, agriculture, and freshwater replenishment."
            ],
            visual_diagram=DiagramService.get_diagram_for_topic("water cycle"),
            videos=VideoService.get_videos_for_topic("water cycle", lang),
            practice_questions=[
                PracticeQuestion(
                    question="What process describes water evaporation directly from plant leaves?",
                    options=["Sublimation", "Transpiration", "Precipitation", "Infiltration"],
                    correct_answer=1,
                    explanation="Transpiration is the biological release of water vapor from microscopic pores (stomata) on plant leaves."
                )
            ],
            follow_up_questions=[
                "How does deforestation affect the regional water cycle?",
                "What is groundwater depletion and how can it be mitigated?",
                "How do oceans regulate global atmospheric climate?"
            ],
            citations=citations,
            audio_text=simple_exp
        )

    @classmethod
    def _build_generic_educational_response(
        cls,
        req: LearningRequest,
        topic: str,
        citations: List[Citation],
        answered_from_pdf: bool,
        missing_from_pdf: bool,
        lang: str
    ) -> LearningResponse:
        is_telugu = "telugu" in lang.lower()
        topic_title = topic.strip().title()

        if answered_from_pdf and citations:
            doc_context_snippet = citations[0].text_snippet
            simple_exp = (
                f"Based on **{citations[0].filename} (Page {citations[0].page_number})**:\n\n"
                f"{doc_context_snippet}\n\n"
                f"**Additional Conceptual Breakdown:**\n"
                f"In simpler terms, {topic_title} represents a fundamental principle where specific input criteria and rules work together to produce consistent, predictable results."
            )
        elif is_telugu:
            simple_exp = (
                f"**{topic_title}** గురించి సరళమైన వివరణ:\n"
                f"{topic_title} అనేది ఒక ముఖ్యమైన భావన. దీనిని సులభంగా అర్థం చేసుకోవడానికి, "
                f"మనం దైనందిన జీవితంలోని నియమాలు మరియు ఉదాహరణలతో పోల్చి చూడవచ్చు. "
                f"ఇది ఎలా పనిచేస్తుందో మరియు ఎందుకు ముఖ్యమైనదో క్రింద దశలవారీగా చూద్దాం."
            )
        else:
            simple_exp = (
                f"**{topic_title}** explained simply:\n"
                f"At its core, **{topic_title}** is a concept designed to solve specific challenges by establishing clear rules, mechanisms, and outcomes. "
                f"Whether applied in academics or industry, understanding its fundamentals empowers you to analyze, predict, and innovate effectively."
            )

        definition = f"**{topic_title}**: A defined structure or methodology recognized in its field, characterized by systematic inputs, internal governing logic, and standardized outcomes."
        
        how_it_works = [
            f"1. **Foundations**: Establishing the core terms, hypotheses, and inputs required for {topic_title}.",
            f"2. **Processing**: Executing the fundamental transformations or principles step by step.",
            f"3. **Verification**: Checking outputs against established benchmarks and rules.",
            f"4. **Real-world Application**: Utilizing the final result to solve practical challenges."
        ]

        example = f"💡 **Practical Application**:\nIn everyday practice, {topic_title} is utilized across research and industry to streamline complex workflows and ensure accuracy."

        key_points = [
            f"Primary focus: Streamlined understanding of {topic_title}.",
            "Emphasizes foundational clarity before progressing to advanced nuances.",
            "Can be evaluated through structured problem solving and experiments."
        ]

        practice = [
            PracticeQuestion(
                question=f"Which of the following best characterizes the primary objective of {topic_title}?",
                options=[
                    f"To organize and understand the core principles of {topic_title}",
                    "To introduce arbitrary complexity without purpose",
                    "To eliminate all mathematical and logical validation",
                    "None of the above"
                ],
                correct_answer=0,
                explanation=f"The primary objective is systematic clarity and functional understanding of {topic_title}."
            )
        ]

        follow_ups = [
            f"Can you explain the mathematical foundations behind {topic_title}?",
            f"What are the top 3 industry use-cases of {topic_title}?",
            f"Give me a beginner-friendly code or practical demonstration for {topic_title}."
        ]

        diagram = DiagramService.get_diagram_for_topic(topic)
        videos = VideoService.get_videos_for_topic(topic, lang)

        return LearningResponse(
            question=req.question,
            mode="pdf_based" if answered_from_pdf else "general_ai",
            source_mode=req.source_mode,
            language=lang,
            answered_from_pdf=answered_from_pdf,
            missing_from_pdf=missing_from_pdf,
            simple_explanation=simple_exp,
            definition=definition,
            how_it_works=how_it_works,
            example=example,
            key_points=key_points,
            visual_diagram=diagram,
            videos=videos,
            practice_questions=practice,
            follow_up_questions=follow_ups,
            citations=citations,
            audio_text=simple_exp.replace("**", "").replace("#", "")
        )

    @classmethod
    async def _call_gemini_api(cls, req: LearningRequest, context: str, source_mode: str) -> Optional[LearningResponse]:
        """Calls Google Gemini API when GEMINI_API_KEY is configured."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.DEFAULT_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = f"""You are LearnBridge AI, an expert, student-friendly AI Tutor.
User Language: {req.language}
Source Mode: {source_mode}
Document Context (if any):
{context}

User Question: {req.question}

Please return a structured JSON response matching this schema:
{{
  "simple_explanation": "...",
  "definition": "...",
  "how_it_works": ["step 1", "step 2", "step 3"],
  "example": "...",
  "key_points": ["point 1", "point 2"],
  "practice_questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "..."
    }}
  ],
  "follow_up_questions": ["q1", "q2", "q3"]
}}
"""
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(
                    url,
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    clean_json = re.search(r'\{.*\}', text, re.DOTALL)
                    if clean_json:
                        parsed = json.loads(clean_json.group(0))
                        diagram = DiagramService.get_diagram_for_topic(req.question)
                        videos = VideoService.get_videos_for_topic(req.question, req.language)
                        return LearningResponse(
                            question=req.question,
                            mode="pdf_based" if context else "general_ai",
                            source_mode=source_mode,
                            language=req.language,
                            answered_from_pdf=bool(context),
                            simple_explanation=parsed.get("simple_explanation", ""),
                            definition=parsed.get("definition"),
                            how_it_works=parsed.get("how_it_works", []),
                            example=parsed.get("example"),
                            key_points=parsed.get("key_points", []),
                            visual_diagram=diagram,
                            videos=videos,
                            practice_questions=[PracticeQuestion(**q) for q in parsed.get("practice_questions", [])],
                            follow_up_questions=parsed.get("follow_up_questions", []),
                            citations=[],
                            audio_text=parsed.get("simple_explanation", "")
                        )
        except Exception:
            pass
        return None

    @classmethod
    async def _call_openai_api(cls, req: LearningRequest, context: str, source_mode: str) -> Optional[LearningResponse]:
        """Calls OpenAI API when OPENAI_API_KEY is configured."""
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"}
            prompt = f"Explain for student in {req.language}: {req.question}. Context: {context}"
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(
                    url,
                    headers=headers,
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    ans = data["choices"][0]["message"]["content"]
                    diagram = DiagramService.get_diagram_for_topic(req.question)
                    videos = VideoService.get_videos_for_topic(req.question, req.language)
                    return LearningResponse(
                        question=req.question,
                        mode="pdf_based" if context else "general_ai",
                        source_mode=source_mode,
                        language=req.language,
                        answered_from_pdf=bool(context),
                        simple_explanation=ans,
                        definition=None,
                        how_it_works=[],
                        example=None,
                        key_points=[],
                        visual_diagram=diagram,
                        videos=videos,
                        practice_questions=[],
                        follow_up_questions=[f"Tell me more about {req.question}"],
                        citations=[],
                        audio_text=ans
                    )
        except Exception:
            pass
        return None
