from fastapi import APIRouter, HTTPException
from ..models import LearningRequest, LearningResponse, QuickActionRequest
from ..services.ai_service import AIService
from ..services.diagram_service import DiagramService
from ..services.video_service import VideoService
from ..services.quiz_service import QuizService

router = APIRouter(prefix="/learning", tags=["Learning"])

@router.post("/ask", response_model=LearningResponse)
async def ask_question(request: LearningRequest):
    """
    Main Learning Endpoint:
    Can be used with OR without a PDF document.
    Supports Regional Languages (Telugu, Hindi, Tamil, etc.),
    Citations, Diagrams, and Videos.
    """
    try:
        response = await AIService.process_learning_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning response: {str(e)}")

@router.post("/quick-action")
async def execute_quick_action(request: QuickActionRequest):
    """
    Executes instant interactive pedagogical actions:
    - simple (Explain in Simple Words)
    - step_by_step (Explain Step by Step)
    - example (Give a Practical Example)
    - my_language (Explain in Regional Language, e.g., Telugu)
    - diagram (Show a Diagram)
    - video (Find Video)
    - quiz (Generate Quiz)
    - summarize (Summarize Key Points)
    """
    topic = request.topic.strip()
    action = request.action.lower()
    target_lang = request.target_language or "Telugu"

    if action == "diagram":
        diag = DiagramService.get_diagram_for_topic(topic)
        return {"action": action, "topic": topic, "diagram": diag}

    elif action == "video":
        vids = VideoService.get_videos_for_topic(topic, preferred_language=target_lang)
        return {"action": action, "topic": topic, "videos": vids}

    elif action == "quiz":
        questions = QuizService.generate_quiz(topic)
        return {"action": action, "topic": topic, "questions": questions}

    elif action == "my_language":
        req = LearningRequest(
            question=f"Explain {topic} in {target_lang}",
            language=target_lang,
            source_mode="general_ai"
        )
        res = await AIService.process_learning_request(req)
        return {"action": action, "topic": topic, "language": target_lang, "response": res}

    elif action == "simple":
        req = LearningRequest(
            question=f"Explain {topic} in very simple words for a beginner",
            detail_level="simple",
            source_mode="general_ai"
        )
        res = await AIService.process_learning_request(req)
        return {"action": action, "topic": topic, "response": res}

    elif action == "step_by_step":
        req = LearningRequest(
            question=f"Explain how {topic} works step by step",
            detail_level="detailed",
            source_mode="general_ai"
        )
        res = await AIService.process_learning_request(req)
        return {"action": action, "topic": topic, "response": res}

    elif action == "example":
        req = LearningRequest(
            question=f"Give everyday real-life examples of {topic}",
            source_mode="general_ai"
        )
        res = await AIService.process_learning_request(req)
        return {"action": action, "topic": topic, "response": res}

    elif action == "summarize":
        req = LearningRequest(
            question=f"Summarize the key points of {topic}",
            source_mode="general_ai"
        )
        res = await AIService.process_learning_request(req)
        return {"action": action, "topic": topic, "response": res}

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported quick action '{action}'")
