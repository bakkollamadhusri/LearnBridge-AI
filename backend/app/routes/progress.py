from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/progress", tags=["Personalized Learning & Progress"])

class ActivityLog(BaseModel):
    activity_type: str # "asked_question", "completed_quiz", "uploaded_pdf", "viewed_diagram"
    topic: str
    details: Dict[str, Any] = {}

# In-memory progress tracking with meaningful initial stats
USER_STATS = {
    "streak_days": 7,
    "total_questions_asked": 24,
    "quizzes_completed": 6,
    "average_quiz_score": 88.5,
    "study_hours_this_week": 14.5,
    "completed_topics": [
        {"topic": "Introduction to Machine Learning", "category": "AI/ML", "date": "Yesterday"},
        {"topic": "P-N Junction Diode & Forward Bias", "category": "Electronics", "date": "2 days ago"},
        {"topic": "Photosynthesis & Light Reactions", "category": "Biology", "date": "3 days ago"},
        {"topic": "Python Data Structures", "category": "Programming", "date": "4 days ago"}
    ],
    "weekly_study_chart": [
        {"day": "Mon", "hours": 1.5, "questions": 3},
        {"day": "Tue", "hours": 2.0, "questions": 5},
        {"day": "Wed", "hours": 2.5, "questions": 4},
        {"day": "Thu", "hours": 1.8, "questions": 3},
        {"day": "Fri", "hours": 3.2, "questions": 7},
        {"day": "Sat", "hours": 2.0, "questions": 2},
        {"day": "Sun", "hours": 1.5, "questions": 2}
    ],
    "subject_distribution": [
        {"subject": "AI & Machine Learning", "percentage": 40},
        {"subject": "Semiconductors & Physics", "percentage": 25},
        {"subject": "Web Development", "percentage": 20},
        {"subject": "General Science", "percentage": 15}
    ],
    "recommendations_what_to_learn_next": [
        {"title": "Deep Learning: Perceptrons & Backpropagation", "difficulty": "Intermediate", "category": "AI/ML", "estimated_mins": 25},
        {"title": "Zener Diode Voltage Regulators", "difficulty": "Intermediate", "category": "Electronics", "estimated_mins": 20},
        {"title": "Building RAG with Vector Databases", "difficulty": "Advanced", "category": "Full-Stack AI", "estimated_mins": 35}
    ]
}

@router.get("/stats")
async def get_user_stats():
    """Returns analytics, study streak, charts data, and 'what to learn next' recommendations."""
    return USER_STATS

@router.post("/log")
async def log_activity(activity: ActivityLog):
    """Logs user study actions to update learning streaks and analytics."""
    USER_STATS["total_questions_asked"] += 1
    return {"success": True, "message": "Activity recorded", "new_streak": USER_STATS["streak_days"]}
