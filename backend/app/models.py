from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

class MessageItem(BaseModel):
    role: str # "user" | "assistant"
    content: str

class LearningRequest(BaseModel):
    question: str
    document_id: Optional[str] = None
    source_mode: str = "pdf_and_ai"  # "pdf_and_ai" | "pdf_only" | "general_ai"
    language: str = "English"  # "English", "Telugu", "Hindi", "Tamil", "English + Telugu", etc.
    education_level: str = "college" # "beginner", "school", "college", "competitive"
    detail_level: str = "standard" # "simple", "standard", "detailed"
    conversation_history: Optional[List[MessageItem]] = []
    user_id: Optional[str] = "guest-user-1"

class Citation(BaseModel):
    document_id: str
    filename: str
    page_number: int
    text_snippet: str
    score: float

class VideoRecommendation(BaseModel):
    title: str
    channel: str
    url: str
    embed_url: Optional[str] = None
    thumbnail_url: str
    duration: str
    language: str
    description: str

class DiagramData(BaseModel):
    type: str # "svg" | "flowchart" | "circuit" | "concept_map"
    title: str
    svg_content: Optional[str] = None
    description: str
    labels: List[str] = []

class PracticeQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class LearningResponse(BaseModel):
    question: str
    mode: str # "general_ai" | "pdf_based"
    source_mode: str
    language: str
    answered_from_pdf: bool = False
    missing_from_pdf: bool = False
    
    # Core Smart Answer Format
    simple_explanation: str
    definition: Optional[str] = None
    how_it_works: Optional[Union[List[str], str]] = None
    example: Optional[str] = None
    key_points: Optional[List[str]] = []
    
    # Media & Visuals
    visual_diagram: Optional[DiagramData] = None
    videos: Optional[List[VideoRecommendation]] = []
    
    # Interactive Practice & Follow-up
    practice_questions: Optional[List[PracticeQuestion]] = []
    follow_up_questions: Optional[List[str]] = []
    
    # RAG Citations
    citations: Optional[List[Citation]] = []
    
    # Spoken Audio Text (Cleaned for TTS)
    audio_text: str

class QuickActionRequest(BaseModel):
    action: str # "simple", "step_by_step", "example", "my_language", "diagram", "video", "quiz", "summarize"
    topic: str
    previous_response: Optional[str] = None
    target_language: Optional[str] = "Telugu"

class DocumentMetadata(BaseModel):
    id: str
    filename: str
    file_size_bytes: int
    total_pages: int
    uploaded_at: datetime
    status: str # "processing" | "ready" | "error"
    error_message: Optional[str] = None
    user_id: str
    summary_preview: Optional[str] = None

class Flashcard(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    mastered: bool = False

class QuizSubmission(BaseModel):
    quiz_id: str
    user_answers: Dict[int, int] # question_index -> chosen_option

class QuizResult(BaseModel):
    quiz_id: str
    total_questions: int
    correct_count: int
    score_percentage: float
    feedback: str
    results_detail: List[Dict[str, Any]]

class MentorProfile(BaseModel):
    id: str
    name: str
    title: str
    institution_or_company: str
    experience_years: int
    rating: float
    review_count: int
    languages: List[str]
    specialties: List[str]
    avatar_url: str
    hourly_rate_inr: int
    is_available: bool

class BookingRequest(BaseModel):
    mentor_id: str
    learner_name: str
    learner_email: str
    preferred_date: str
    preferred_time: str
    topic_description: str

class StudyGroup(BaseModel):
    id: str
    title: str
    subject: str
    member_count: int
    max_members: int
    meeting_schedule: str
    active_now: bool
    description: str
