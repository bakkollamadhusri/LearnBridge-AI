# MASTER PROMPT: Build LearnBridge AI — An AI-Powered Personalized Learning Platform

Act as a senior full-stack developer, AI engineer, UI/UX designer, and software architect. Build a complete, functional, responsive AI-powered learning platform called **LearnBridge AI**.

**Tagline:** Learn Anything. Connect with Everyone. Grow Together.

Do not create only a landing page or static UI prototype. Build a working application with a real frontend, backend, AI integration, database, and functional learning features.

## 1. First Inspect the Existing Project

Before writing code:

* Inspect the current project structure, existing files, framework, dependencies, and implemented features.
* Reuse the existing architecture and working code wherever possible.
* Do not delete working features or unnecessarily rebuild the project.
* Identify missing features and implement them systematically.
* If the project is empty, initialize a suitable project using the stack below.
* Run the application, test it, fix errors, and verify that the features work end to end.

## 2. Recommended Technology Stack

Use the following stack where compatible with the existing project:

**Frontend**

* Next.js, React, and TypeScript.
* Tailwind CSS and shadcn/ui.
* Lucide icons.
* Recharts for progress charts.
* Responsive layouts for desktop, tablet, and mobile.

**Backend**

* Python FastAPI.
* REST APIs with request validation and error handling.
* Configurable AI model provider.
* Separate services for AI chat, RAG, image generation, video retrieval, and text-to-speech.

**Database and storage**

* Supabase PostgreSQL.
* Supabase Auth for authentication.
* Supabase Storage for uploaded documents and permitted user files.
* PostgreSQL with pgvector for document embeddings when required.
* Row-level security and user-specific document access.

Use environment variables for API keys. Never expose secret keys in frontend code. If an external service requires credentials, provide setup instructions and graceful fallback behavior.

## 3. Main Requirement: AI Learning With or Without a PDF

This is the most important feature.

The learner must be able to ask any question without uploading a document. PDF upload is optional, not compulsory.

Create two learning modes:

### Mode A: General AI Learning — No PDF Required

When the learner asks a question without selecting a PDF:

* Answer using the configured AI model's general knowledge.
* Explain the concept in simple, student-friendly language.
* Provide a definition, step-by-step explanation, examples, and real-world applications when useful.
* Give the learner an option to request a simpler explanation or a more detailed explanation.
* Support follow-up questions using the conversation history.
* Do not ask the learner to upload a PDF before answering.
* Do not invent PDF citations or claim that information came from a document.
* Clearly identify the answer as a general AI explanation when source identification is relevant.

Example:

User: "Explain machine learning in Telugu."

The AI should explain machine learning in simple Telugu, provide an everyday example, and offer a suitable visual or audio explanation when available.

### Mode B: PDF-Based Learning

When the learner uploads and selects a PDF:

* Extract the document text.
* Use Retrieval-Augmented Generation (RAG) to retrieve relevant passages.
* Answer questions using the selected PDF as the primary source.
* Display the filename and correct page numbers for supporting passages.
* Separate document-supported information from additional general AI knowledge.
* If the answer is missing from the PDF, explicitly state that it was not found in the document and offer a separate general AI answer.
* Never fabricate citations, page numbers, quotations, or document content.
* Ensure content from different users' documents or unrelated PDFs is never mixed.

Add a clear source selector with these modes:

1. **PDF + AI Knowledge** — Default when a PDF is selected. Use the PDF first and add clearly separated general knowledge when useful.
2. **PDF Only** — Answer strictly from retrieved PDF content. If evidence is insufficient, say so.
3. **General AI** — Answer from general AI knowledge without treating the PDF as evidence.

When no PDF is selected, automatically use General AI mode.

## 4. PDF Upload and RAG Implementation

Build a fully working document-question-answering feature.

**Upload interface**

* Upload button and drag-and-drop area.
* Accept PDF files and validate type and file size.
* Show filename, file size, upload progress, and processing status.
* Show useful error messages for unsupported, corrupted, empty, or oversized files.
* Allow users to select, switch between, and delete their own uploaded documents.

**Document processing**

* Use PyMuPDF to extract text from every page.
* Preserve original page numbers.
* Detect scanned or image-based PDFs and support OCR when an OCR service or library is configured.
* Divide extracted text into overlapping chunks.
* Generate embeddings using a configured embedding model.
* Store chunks, embeddings, document IDs, ownership metadata, and page numbers in PostgreSQL with pgvector.

**Question-answering workflow**

1. Receive the question and selected document ID.
2. Check document ownership and processing status.
3. Retrieve relevant chunks from only the selected document.
4. Send the retrieved context and question to the configured AI model.
5. Generate a grounded answer.
6. Return citations linked to actual retrieved chunks.
7. Display source citations below the answer.
8. Preserve document context during follow-up questions.

Suggested endpoints:

* `POST /api/documents/upload`
* `GET /api/documents`
* `GET /api/documents/{document_id}/status`
* `POST /api/documents/{document_id}/ask`
* `DELETE /api/documents/{document_id}`
* `POST /api/learning/ask`

Implement proper authentication, access control, file validation, timeouts, error handling, and ownership checks.

## 5. Regional Language Learning

Add a language selector to the main learning interface.

Support these languages when the configured AI model supports them:

* English
* Telugu
* Hindi
* Tamil
* Kannada
* Malayalam
* Marathi
* Bengali
* Other supported languages.

Requirements:

* Allow users to ask questions in their preferred language.
* Explain answers naturally in the selected language.
* Provide an English + regional language option.
* Translate definitions, examples, summaries, quizzes, and follow-up explanations when requested.
* Explain technical terms instead of translating them incorrectly.
* Preserve mathematical formulas, programming syntax, scientific notation, and code.
* Use a language preference stored in the user's profile, with an easy way to change it.
* Use an appropriate text-to-speech voice for the selected language when available.
* Do not claim language or voice support if the configured service does not provide it.

Example language selection:

* Telugu
* English
* English + Telugu

## 6. AI Tutor and Smart Answer Format

Create a conversational AI tutor that can answer academic, technical, general knowledge, and practical questions.

For a typical learning question, provide the following sections when appropriate:

1. **Simple Explanation** — Explain the concept in easy words.
2. **Definition** — Give a clear, accurate definition.
3. **How It Works** — Explain step by step.
4. **Example** — Give a practical or real-life example.
5. **Visual Explanation** — Provide an image or diagram when useful.
6. **Watch and Listen** — Offer relevant video or audio when available.
7. **Key Points** — Summarize the most important information.
8. **Practice Questions** — Offer a quiz or practice problem.
9. **Follow-up Questions** — Let the learner explore the topic further.

Do not force all nine sections into every response. Adapt the answer to the user's question, learning level, and preferences.

Provide quick actions:

* Explain in Simple Words
* Explain Step by Step
* Give an Example
* Explain in My Language
* Show a Diagram
* Listen to Explanation
* Find a Video
* Summarize
* Generate a Quiz

## 7. Educational Images and Diagrams

When a visual would improve understanding, generate or retrieve a relevant educational image.

Examples:

* PN junction diode with labelled P-type, N-type, and depletion regions.
* Photosynthesis with labelled plant structures.
* Water cycle with arrows and labels.
* Neural network with input, hidden, and output layers.
* Flowcharts for algorithms.
* Mathematical graphs and geometry diagrams.
* Circuit diagrams for electronics.
* Illustrations of scientific processes.

Requirements:

* Use an available image-generation service for original illustrations.
* Use reliable image retrieval when an existing image is more suitable.
* Prefer clear, readable diagrams with labels and captions.
* Explain what the visual demonstrates.
* Generate separate visuals for distinct concepts when needed.
* Use appropriate image licensing and attribution for retrieved content.
* Never invent an image source or claim an image has been generated if generation failed.
* If image generation or retrieval is unavailable, provide a text-based explanation or a programmatically rendered diagram where appropriate.

Do not generate an image for every simple question. Use visuals when they provide genuine learning value.

## 8. Educational Videos

When a topic benefits from a video, find a relevant educational video using an available search API or supported video integration.

Requirements:

* Show the real video title, provider, thumbnail, language, and source link.
* Prefer educational and trustworthy sources.
* Prefer videos in the learner's selected language when suitable options exist.
* Prefer videos with spoken explanations and captions or subtitles.
* Use embedded playback only when permitted by the provider.
* Do not fabricate video URLs, titles, thumbnails, or transcripts.
* Do not download copyrighted videos without authorization.
* If no suitable video is found, show a helpful message and continue with the text and visual explanation.

The user should be able to click a real video link or play the video when embedding is supported.

## 9. Audio Explanations and Text-to-Speech

Add a **Listen to Explanation** button to AI answers.

Use a configured text-to-speech provider or supported browser speech capability.

Implement:

* Play.
* Pause and resume, where supported.
* Stop.
* Language selection.
* Suitable available voices.
* Readable text displayed alongside the audio.
* Clear error handling if the selected language or audio service is unavailable.

Audio must be generated from the actual answer. Do not play placeholder audio or claim an unavailable audio feature is working.

For educational videos, use the provider's real audio and captions when available. Do not claim that a video contains spoken explanations unless that is supported by reliable metadata or inspection.

## 10. Additional Learning Features

Implement these features as working modules where feasible:

**AI-generated study materials**

* Topic summaries.
* Notes.
* Flashcards.
* Multiple-choice quizzes.
* Short-answer questions.
* Practice tests with explanations.
* Revision plans.

**Personalized learning**

* Let learners select their education level and topics of interest.
* Offer personalized learning paths.
* Track completed topics and quiz scores.
* Display progress charts and learning streaks.
* Recommend what to learn next.

**Career guidance**

* Skill-learning roadmaps.
* Programming and technical interview preparation.
* Resume and interview practice.
* Project suggestions based on interests and skill level.

**Community learning**

* Study groups.
* Mentor discovery.
* Mentor session requests.
* Teacher and mentor profiles.

Do not build fake features that appear functional but do nothing. If a feature requires a separate integration or later implementation, label its status clearly.

## 11. UI/UX Design

Create a modern, attractive, professional learning experience.

Use:

* A clean layout with a clear visual hierarchy.
* A friendly, accessible color palette.
* Readable typography.
* Rounded cards and consistent spacing.
* Responsive navigation.
* Accessible buttons and form controls.
* Loading states, empty states, and error messages.
* Dark and light themes if compatible with the current application.

Suggested pages:

1. Landing page.
2. Sign-up and login.
3. Learner dashboard.
4. AI learning workspace.
5. PDF library and document chat.
6. Saved notes and flashcards.
7. Quizzes and practice tests.
8. Learning progress dashboard.
9. Profile and language settings.
10. Mentor and study-group area.

**Main learning workspace layout**

* Conversation and question input.
* Optional PDF upload and document selector.
* Source-mode selector.
* Regional language selector.
* AI response area.
* Relevant image or diagram area.
* Video and audio controls when available.
* Suggested follow-up questions.

Use the placeholder:

"Ask anything you want to learn, in your preferred language..."

Make PDF upload optional and visually distinct from the question input.

## 12. Database, Security, and Privacy

Implement:

* Secure authentication.
* User profiles and language preferences.
* Conversation history.
* Uploaded document metadata.
* Document chunks, embeddings, and page references.
* Saved notes, flashcards, quizzes, and progress records.
* Proper database relationships and migrations.
* Row-level security and server-side authorization.
* File type and size validation.
* Rate limits and sensible request limits.
* Safe handling of user uploads and model outputs.
* Server-side secret management.

Do not expose API keys, private PDF content, or another user's data. Never use one user's uploaded documents to answer another user's questions without explicit authorization.

## 13. Environment Setup and Deployment

Create a `.env.example` file with all required configuration variables, without real secrets.

Document the required configuration for:

* Supabase URL and keys.
* AI model API.
* Embedding model.
* Image-generation provider.
* Video search provider, if required.
* Text-to-speech provider.
* OCR configuration, if required.

Reuse one compatible AI provider where possible, but keep services modular so they can be replaced.

Prepare the project for deployment with a suitable frontend host, Python backend host, and Supabase services.

Include a README explaining installation, configuration, migrations, running the application, testing, and deployment.

If credentials are missing, finish the code that can be implemented, clearly identify the missing configuration, and explain how to supply it. Never fabricate API responses or credentials.

## 14. Testing and Acceptance Criteria

Test the actual application, not just individual UI components.

Required tests:

1. Ask a question without uploading a PDF and receive a general AI answer.
2. Ask for an explanation in Telugu.
3. Request an English + Telugu explanation.
4. Ask a follow-up question and verify context is preserved.
5. Upload a text-based PDF and ask a question answered in the document.
6. Verify that PDF citations reference the correct pages.
7. Ask a question not answered by the PDF and verify the separation between missing document information and general AI knowledge.
8. Switch between PDFs and verify that document contexts are not mixed.
9. Generate a summary, flashcards, and quiz.
10. Request an educational diagram.
11. Request a relevant educational video.
12. Play an audio explanation where audio is configured.
13. Test unavailable media services and verify that text learning continues to work.
14. Test invalid uploads, empty documents, and failed API calls.
15. Verify authentication and prevent unauthorized document access.
16. Check the responsive interface on mobile and desktop.
17. Run available frontend and backend tests and fix implementation errors.

## 15. Final Instructions

Work in phases:

**Phase 1:** Inspect the existing project and establish the architecture.

**Phase 2:** Build the core UI, authentication, database, and general AI question-answering workflow.

**Phase 3:** Implement PDF upload, RAG, citations, and document isolation.

**Phase 4:** Add regional languages, educational images, video discovery, and audio explanations.

**Phase 5:** Add study materials, quizzes, progress tracking, and other learning features.

**Phase 6:** Run tests, fix bugs, document setup, and prepare deployment.

Prioritize a reliable, working core application before adding advanced features.

Do not stop after producing a plan. Start implementing the project, run it, inspect errors, and continue fixing them. At the end, report:

* Features actually implemented.
* Features tested successfully.
* Files and architecture created or modified.
* Required environment variables and API keys.
* Any features that remain incomplete and why.
* Exact steps to run the application locally.

**Final goal:** Deliver a functional LearnBridge AI learning platform that allows anyone to ask a question and understand the answer through simple explanations, examples, regional languages, educational visuals, and available video or audio—even without uploading a PDF.