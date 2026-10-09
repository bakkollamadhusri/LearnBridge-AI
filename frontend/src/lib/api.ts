import {
  LearningResponse,
  DocumentMetadata,
  Flashcard,
  PracticeQuestion,
  MentorProfile,
  StudyGroup,
  LearningStats,
  SourceMode
} from '../types';

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function askQuestion(params: {
  question: string;
  document_id?: string | null;
  source_mode?: SourceMode;
  language?: string;
  education_level?: string;
  conversation_history?: Array<{ role: string; content: string }>;
}): Promise<LearningResponse> {
  const res = await fetch(`${BASE_URL}/api/learning/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question: params.question,
      document_id: params.document_id || null,
      source_mode: params.source_mode || 'pdf_and_ai',
      language: params.language || 'English',
      education_level: params.education_level || 'college',
      conversation_history: params.conversation_history || []
    })
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Network request failed' }));
    throw new Error(errorData.detail || 'Failed to fetch AI response');
  }

  return res.json();
}

export async function uploadPDF(file: File, userId: string = 'guest-user-1'): Promise<DocumentMetadata> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);

  const res = await fetch(`${BASE_URL}/api/documents/upload`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Failed to upload document');
  }

  return res.json();
}

export async function fetchDocuments(userId: string = 'guest-user-1'): Promise<DocumentMetadata[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/documents?user_id=${userId}`);
    if (res.ok) {
      return res.json();
    }
  } catch {
    // Graceful fallback
  }
  return [];
}

export async function deleteDocument(docId: string, userId: string = 'guest-user-1'): Promise<boolean> {
  const res = await fetch(`${BASE_URL}/api/documents/${docId}?user_id=${userId}`, {
    method: 'DELETE'
  });
  return res.ok;
}

export async function fetchFlashcards(topic: string = 'Machine Learning'): Promise<Flashcard[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/study/flashcards?topic=${encodeURIComponent(topic)}`);
    if (res.ok) {
      return res.json();
    }
  } catch {}
  return [];
}

export async function fetchQuiz(topic: string = 'Machine Learning'): Promise<PracticeQuestion[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/study/quiz?topic=${encodeURIComponent(topic)}`);
    if (res.ok) {
      return res.json();
    }
  } catch {}
  return [];
}

export async function submitQuizAnswers(topic: string, answers: Record<number, number>) {
  const res = await fetch(`${BASE_URL}/api/study/quiz/submit?topic=${encodeURIComponent(topic)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(answers)
  });
  return res.json();
}

export async function fetchMentors(): Promise<MentorProfile[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/community/mentors`);
    if (res.ok) {
      return res.json();
    }
  } catch {}
  return [];
}

export async function fetchStudyGroups(): Promise<StudyGroup[]> {
  try {
    const res = await fetch(`${BASE_URL}/api/community/groups`);
    if (res.ok) {
      return res.json();
    }
  } catch {}
  return [];
}

export async function bookMentorSession(booking: {
  mentor_id: string;
  learner_name: string;
  learner_email: string;
  preferred_date: string;
  preferred_time: string;
  topic_description: string;
}) {
  const res = await fetch(`${BASE_URL}/api/community/book-mentor`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(booking)
  });
  return res.json();
}

export async function fetchProgressStats(): Promise<LearningStats> {
  const res = await fetch(`${BASE_URL}/api/progress/stats`);
  if (res.ok) {
    return res.json();
  }
  throw new Error('Failed to load progress');
}

export async function fetchRoadmap(topic: string = 'Full-Stack AI Developer') {
  const res = await fetch(`${BASE_URL}/api/study/roadmap?topic=${encodeURIComponent(topic)}`);
  return res.json();
}
