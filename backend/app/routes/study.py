from typing import List, Dict
from fastapi import APIRouter, Query, HTTPException
from ..models import Flashcard, PracticeQuestion, QuizResult
from ..services.quiz_service import QuizService

router = APIRouter(prefix="/study", tags=["Study Materials & Quizzes"])

# Cache in-memory active quizzes for submission scoring
ACTIVE_QUIZZES: Dict[str, List[PracticeQuestion]] = {}

@router.get("/flashcards", response_model=List[Flashcard])
async def get_flashcards(topic: str = Query("Machine Learning"), count: int = Query(5)):
    """Generates study flashcards for a given topic."""
    cards = QuizService.generate_flashcards(topic=topic, count=count)
    return cards

@router.get("/quiz", response_model=List[PracticeQuestion])
async def get_quiz(topic: str = Query("Machine Learning")):
    """Generates interactive quiz questions for a topic."""
    questions = QuizService.generate_quiz(topic=topic)
    # Store for scoring
    ACTIVE_QUIZZES[topic.lower()] = questions
    return questions

@router.post("/quiz/submit", response_model=QuizResult)
async def submit_quiz(
    topic: str,
    user_answers: Dict[int, int]
):
    """Evaluates quiz submissions and provides detailed feedback."""
    questions = ACTIVE_QUIZZES.get(topic.lower())
    if not questions:
        questions = QuizService.generate_quiz(topic=topic)
    
    result = QuizService.evaluate_quiz(
        quiz_id=topic,
        questions=questions,
        user_answers=user_answers
    )
    return result

@router.get("/roadmap")
async def get_learning_roadmap(topic: str = Query("Full-Stack AI Developer")):
    """Generates a structured career and skill learning roadmap."""
    topic_lower = topic.lower()
    if "ai" in topic_lower or "machine learning" in topic_lower or "ml" in topic_lower:
        steps = [
            {"step": 1, "phase": "Foundations", "title": "Mathematics & Python Basics", "skills": ["Linear Algebra", "Calculus", "Python 3", "NumPy", "Pandas"], "weeks": 3},
            {"step": 2, "phase": "Classical ML", "title": "Supervised & Unsupervised Algorithms", "skills": ["Scikit-Learn", "Regression", "Decision Trees", "Ensemble Methods"], "weeks": 4},
            {"step": 3, "phase": "Deep Learning", "title": "Neural Networks & Architectures", "skills": ["PyTorch / TensorFlow", "CNNs", "RNNs", "Transformers"], "weeks": 5},
            {"step": 4, "phase": "Modern AI & RAG", "title": "LLMs, Vector Databases & RAG", "skills": ["Prompt Engineering", "Embeddings", "pgvector", "LangChain/FastAPI"], "weeks": 4},
            {"step": 5, "phase": "Production MLOps", "title": "Deployment & Monitoring", "skills": ["Docker", "Model Serving", "FastAPI", "Cloud Deployment"], "weeks": 3}
        ]
    elif "web" in topic_lower or "full" in topic_lower or "developer" in topic_lower:
        steps = [
            {"step": 1, "phase": "Core Web", "title": "HTML5, CSS3 & Modern JavaScript", "skills": ["Semantic HTML", "Tailwind CSS", "ES6+ Async/Await", "DOM Manipulation"], "weeks": 3},
            {"step": 2, "phase": "Frontend Frameworks", "title": "React, Next.js & TypeScript", "skills": ["React Hooks", "Next.js App Router", "State Management", "TypeScript Typing"], "weeks": 4},
            {"step": 3, "phase": "Backend Engineering", "title": "REST APIs & Data Services", "skills": ["Python FastAPI / Node.js", "Pydantic", "Authentication & JWT", "PostgreSQL"], "weeks": 4},
            {"step": 4, "phase": "System Architecture", "title": "Databases, Caching & Cloud", "skills": ["Supabase / PostgreSQL", "Redis", "Row Level Security", "Git Workflows"], "weeks": 3},
            {"step": 5, "phase": "Full-Stack Capstone", "title": "AI Integration & Production", "skills": ["LLM API Integration", "CI/CD", "Vercel / Cloud Deployment", "Testing"], "weeks": 3}
        ]
    else:
        steps = [
            {"step": 1, "phase": "Fundamentals", "title": f"Basics of {topic.title()}", "skills": ["Core Terminology", "Key Concepts", "Initial Setup"], "weeks": 2},
            {"step": 2, "phase": "Intermediate", "title": f"Hands-on Practice with {topic.title()}", "skills": ["Problem Solving", "Real-world Exercises", "Frameworks"], "weeks": 4},
            {"step": 3, "phase": "Advanced", "title": f"Mastery & Optimization of {topic.title()}", "skills": ["System Design", "Best Practices", "Capstone Project"], "weeks": 4}
        ]

    return {
        "career_track": topic.title(),
        "total_estimated_weeks": sum(s["weeks"] for s in steps),
        "phases": steps
    }
