# LearnBridge AI — AI-Powered Personalized Learning Platform

> **Tagline:** Learn Anything. Connect with Everyone. Grow Together.

LearnBridge AI is a full-stack, responsive, multilingual educational platform combining conversational AI tutoring, precision Retrieval-Augmented Generation (RAG) with PyMuPDF, interactive SVG vector diagrams, authentic educational video discovery, audio speech explanations, practice quizzes, and peer mentor circles.

---

## 🌟 Key Features

1. **AI Learning With or Without a PDF (Core Requirement)**
   - **General AI Mode (Default):** Ask any academic or technical question without uploading documents. Get student-friendly explanations, definitions, step-by-step logic, real-world examples, diagrams, and quizzes.
   - **PDF + AI Knowledge Mode:** When a PDF is selected, retrieve relevant passages with exact page citations and augment with broad AI knowledge.
   - **PDF Only Mode (Strict Grounding):** Strictly answers from retrieved PDF content. Refuses hallucination and clearly informs the user if information is absent from the document.
   - Zero crosstalk: documents are strictly isolated by document ID and user ID.

2. **Regional Language Learning**
   - Native support for **Telugu**, **Hindi**, **Tamil**, **Kannada**, **Malayalam**, **Marathi**, **Bengali**, and **English + Regional** (bilingual mode).
   - Technical terms are preserved and clearly explained instead of being awkwardly translated.

3. **Smart 9-Section Answer Structure**
   - **Simple Explanation** — Concept in plain language
   - **Definition** — Formal accurate definition
   - **How It Works** — Sequential steps and mechanisms
   - **Example** — Practical everyday analogies
   - **Visual Explanation** — Interactive vector SVG diagrams (P-N junctions, Photosynthesis, Neural Networks, Water Cycles, Flowcharts)
   - **Watch & Listen** — Real educational YouTube tutorials with channel, thumbnail, and duration
   - **Key Points** — Quick revision bullets
   - **Practice Questions** — Interactive multiple-choice questions with instant scoring and explanations
   - **Follow-up Questions** — Context-aware follow-up prompts

4. **Speech Narration & TTS**
   - In-browser Web Speech API audio synthesis with Play, Pause/Resume, and Stop controls.

5. **Study Materials & Flashcards**
   - Spaced repetition 3D flip card deck with mastery tracking and category filters.

6. **Interactive Quizzes**
   - Instant scoring, per-question explanations, and celebratory confetti animations.

7. **Learner Analytics & Dashboard**
   - Visualized with **Recharts** (weekly study time bar chart, subject distribution pie chart, study streak counter, and "What to Learn Next" recommendations).

8. **Career Roadmaps & Community Mentors**
   - Skill pathways (Full-Stack AI Developer, ML Engineer, Web Developer) with week-by-week phases.
   - Verified mentor profiles with ratings, regional languages, and 1-on-1 session booking modals.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons, Recharts, Canvas-Confetti |
| **Backend** | Python 3.13/3.15, FastAPI, Uvicorn, PyMuPDF (fitz), Pydantic v2, HTTPX |
| **RAG & Search** | PyMuPDF page-by-page extraction, BM25 / token similarity with stop-word filtering, strict document isolation |
| **Database & Auth** | Supabase PostgreSQL schema with `pgvector` extension, Row-Level Security (RLS) policies (`supabase/schema.sql`) |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v20+ or v24 LTS (`node -v`)
- **Python**: 3.10+ (`python --version` or `py --version`)

### 2. Automated One-Click Start (Windows)
Double-click:
```bash
start-app.bat
```
This automatically launches both the FastAPI backend and Next.js frontend in separate terminal windows.

---

### 3. Manual Step-by-Step Start

#### A. Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Install dependencies
py -m pip install -r requirements.txt

# Run the backend server
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base: `http://127.0.0.1:8000`
- Swagger Interactive Documentation: `http://127.0.0.1:8000/docs`

#### B. Frontend Setup
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Run the development server
npm run dev
```
- Open browser at: `http://localhost:3000`

---

## 🧪 Running Automated Verification Tests

The backend includes an automated test suite verifying all 10 core master prompt requirements:
```powershell
cd backend
py test_backend.py
```
Tests pass for:
- General AI question without PDF
- Telugu regional translation
- Bilingual English + Telugu synthesis
- PDF page extraction and chunking
- PDF citation matching
- Strict "PDF Only" absent-query non-hallucination
- Multi-document and multi-user isolation
- SVG vector diagram generation
- Educational video recommendation with language prioritization
- Flashcard decks and interactive quiz evaluation

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` in the root folder:
```bash
cp .env.example .env
```
Key configuration parameters:
- `AI_PROVIDER`: "gemini", "openai", or "builtin" (runs out-of-the-box without keys)
- `GEMINI_API_KEY`: Optional Google Gemini API key
- `OPENAI_API_KEY`: Optional OpenAI API key
- `NEXT_PUBLIC_SUPABASE_URL`: Optional Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Optional Supabase anon key
- `NEXT_PUBLIC_BACKEND_URL`: `http://127.0.0.1:8000`
