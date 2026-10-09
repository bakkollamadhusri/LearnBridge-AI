export type SourceMode = 'pdf_and_ai' | 'pdf_only' | 'general_ai';

export interface Citation {
  document_id: string;
  filename: string;
  page_number: number;
  text_snippet: string;
  score: number;
}

export interface VideoRecommendation {
  title: string;
  channel: string;
  url: string;
  embed_url?: string;
  thumbnail_url: string;
  duration: string;
  language: string;
  description: string;
}

export interface DiagramData {
  type: string;
  title: string;
  svg_content?: string;
  description: string;
  labels: string[];
}

export interface PracticeQuestion {
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
}

export interface LearningResponse {
  question: string;
  mode: 'general_ai' | 'pdf_based';
  source_mode: SourceMode;
  language: string;
  answered_from_pdf: boolean;
  missing_from_pdf: boolean;
  simple_explanation: string;
  definition?: string;
  how_it_works?: string[] | string;
  example?: string;
  key_points?: string[];
  visual_diagram?: DiagramData;
  videos?: VideoRecommendation[];
  practice_questions?: PracticeQuestion[];
  follow_up_questions?: string[];
  citations?: Citation[];
  audio_text: string;
}

export interface DocumentMetadata {
  id: string;
  filename: string;
  file_size_bytes: number;
  total_pages: number;
  uploaded_at: string;
  status: 'processing' | 'ready' | 'error';
  error_message?: string;
  user_id: string;
  summary_preview?: string;
}

export interface Flashcard {
  id: string;
  question: string;
  answer: string;
  category: string;
  mastered: boolean;
}

export interface MentorProfile {
  id: string;
  name: string;
  title: string;
  institution_or_company: string;
  experience_years: number;
  rating: number;
  review_count: number;
  languages: string[];
  specialties: string[];
  avatar_url: string;
  hourly_rate_inr: number;
  is_available: boolean;
}

export interface StudyGroup {
  id: string;
  title: string;
  subject: string;
  member_count: number;
  max_members: number;
  meeting_schedule: string;
  active_now: boolean;
  description: string;
}

export interface LearningStats {
  streak_days: number;
  total_questions_asked: number;
  quizzes_completed: number;
  average_quiz_score: number;
  study_hours_this_week: number;
  completed_topics: Array<{ topic: string; category: string; date: string }>;
  weekly_study_chart: Array<{ day: string; hours: number; questions: number }>;
  subject_distribution: Array<{ subject: string; percentage: number }>;
  recommendations_what_to_learn_next: Array<{
    title: string;
    difficulty: string;
    category: string;
    estimated_mins: number;
  }>;
}
