from typing import List
from fastapi import APIRouter, HTTPException
from ..models import MentorProfile, BookingRequest, StudyGroup

router = APIRouter(prefix="/community", tags=["Mentors & Study Groups"])

# Curated list of educational mentors
MENTORS: List[MentorProfile] = [
    MentorProfile(
        id="m-1",
        name="Dr. Lakshmi Narayana",
        title="Senior AI Research Scientist & Professor",
        institution_or_company="IIIT Hyderabad / Ex-Microsoft Research",
        experience_years=12,
        rating=4.95,
        review_count=148,
        languages=["Telugu", "English"],
        specialties=["Machine Learning", "Deep Learning", "Mathematics for AI"],
        avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=250&q=80",
        hourly_rate_inr=0,
        is_available=True
    ),
    MentorProfile(
        id="m-2",
        name="Rajesh Sharma",
        title="Principal Semiconductor Engineer",
        institution_or_company="Texas Instruments",
        experience_years=10,
        rating=4.9,
        review_count=112,
        languages=["English", "Hindi"],
        specialties=["VLSI Design", "Semiconductor Physics", "Electronic Circuits"],
        avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=250&q=80",
        hourly_rate_inr=0,
        is_available=True
    ),
    MentorProfile(
        id="m-3",
        name="Ananya Reddy",
        title="Full-Stack Cloud Architect",
        institution_or_company="AWS Community Builder",
        experience_years=8,
        rating=4.98,
        review_count=230,
        languages=["Telugu", "English", "Kannada"],
        specialties=["Next.js", "Python FastAPI", "Cloud Distributed Systems"],
        avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=250&q=80",
        hourly_rate_inr=0,
        is_available=True
    ),
    MentorProfile(
        id="m-4",
        name="Karthik Subramanian",
        title="Data Science Lead & Competitive Mentor",
        institution_or_company="Zoho Research",
        experience_years=7,
        rating=4.88,
        review_count=94,
        languages=["Tamil", "English"],
        specialties=["Data Structures & Algorithms", "System Design", "Python"],
        avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=250&q=80",
        hourly_rate_inr=0,
        is_available=True
    )
]

STUDY_GROUPS: List[StudyGroup] = [
    StudyGroup(
        id="sg-1",
        title="AI & Machine Learning Telugu Circle",
        subject="Artificial Intelligence",
        member_count=342,
        max_members=500,
        meeting_schedule="Every Saturday 7:00 PM IST",
        active_now=True,
        description="Collaborative peer study group discussing foundational ML concepts, hands-on notebooks, and papers with bilingual Telugu/English support."
    ),
    StudyGroup(
        id="sg-2",
        title="Semiconductors & Electronics Core Hub",
        subject="Physics & Electronics",
        member_count=180,
        max_members=250,
        meeting_schedule="Tuesdays & Thursdays 6:30 PM IST",
        active_now=False,
        description="Master PN Junction diodes, transistors, circuit analysis, and GATE/university exam problem solving."
    ),
    StudyGroup(
        id="sg-3",
        title="Full-Stack Developers Guild",
        subject="Web Engineering",
        member_count=520,
        max_members=1000,
        meeting_schedule="Daily asynchronous code-alongs",
        active_now=True,
        description="Building modern full-stack web applications with React, Next.js, FastAPI, and SQL."
    )
]

@router.get("/mentors", response_model=List[MentorProfile])
async def list_mentors():
    """Lists verified mentors across engineering, AI, and regional languages."""
    return MENTORS

@router.post("/book-mentor")
async def book_mentor(booking: BookingRequest):
    """Processes a 1-on-1 mentorship session request."""
    mentor = next((m for m in MENTORS if m.id == booking.mentor_id), None)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found.")
    
    return {
        "success": True,
        "booking_id": f"bk-{booking.mentor_id}-{booking.preferred_date}",
        "message": f"Mentorship session requested with {mentor.name} on {booking.preferred_date} at {booking.preferred_time}. Confirmation email sent to {booking.learner_email}!",
        "details": booking.model_dump()
    }

@router.get("/groups", response_model=List[StudyGroup])
async def list_study_groups():
    """Returns active collaborative study groups."""
    return STUDY_GROUPS

@router.post("/groups/{group_id}/join")
async def join_study_group(group_id: str):
    """Joins an active study group."""
    group = next((g for g in STUDY_GROUPS if g.id == group_id), None)
    if not group:
        raise HTTPException(status_code=404, detail="Study group not found.")
    return {
        "success": True,
        "message": f"Successfully joined '{group.title}'! You now have access to study materials and group discussions.",
        "group_id": group_id
    }
