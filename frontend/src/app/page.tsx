'use client';

import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  BookOpen,
  FileText,
  BarChart3,
  Layers,
  Award,
  Users,
  Compass,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Globe2
} from 'lucide-react';
import { Navbar } from '../components/Navbar';
import { LearningWorkspace } from '../components/LearningWorkspace';
import { PDFManager } from '../components/PDFManager';
import { FlashcardDeck } from '../components/FlashcardDeck';
import { QuizView } from '../components/QuizModal';
import { ProgressDashboard } from '../components/ProgressDashboard';
import { CareerRoadmap } from '../components/CareerRoadmap';
import { CommunityMentors } from '../components/CommunityMentors';
import { DocumentMetadata } from '../types';
import { fetchDocuments } from '../lib/api';

export default function Home() {
  const [activeTab, setActiveTab] = useState('workspace');
  const [selectedLanguage, setSelectedLanguage] = useState('Telugu');
  const [educationLevel, setEducationLevel] = useState('College / Undergraduate');
  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [activeDocumentId, setActiveDocumentId] = useState<string | null>(null);
  const [quizTopic, setQuizTopic] = useState<string>('Machine Learning');
  const streakDays = 7;

  // Initial load of documents
  useEffect(() => {
    fetchDocuments().then((docs) => {
      setDocuments(docs);
      if (docs.length > 0) {
        // We do not auto-select, keeping General AI as default per master prompt requirement!
      }
    });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
        educationLevel={educationLevel}
        setEducationLevel={setEducationLevel}
        streakDays={streakDays}
      />

      {/* Main Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Banner when on Workspace tab */}
        {activeTab === 'workspace' && (
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-950/70 via-slate-900 to-slate-950 border border-indigo-500/30 p-6 md:p-8 shadow-2xl">
            {/* Background glowing orbs */}
            <div className="absolute -top-24 -right-24 h-64 w-64 rounded-full bg-indigo-500/20 blur-3xl pointer-events-none" />
            <div className="absolute -bottom-24 -left-24 h-64 w-64 rounded-full bg-emerald-500/15 blur-3xl pointer-events-none" />

            <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="space-y-3 max-w-3xl">
                <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-bold">
                  <Sparkles className="h-3.5 w-3.5 text-indigo-400 animate-spin" />
                  <span>AI Learning with or without a PDF</span>
                </div>
                <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight leading-tight">
                  Learn Anything.{' '}
                  <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-emerald-400 bg-clip-text text-transparent">
                    Connect with Everyone.
                  </span>{' '}
                  Grow Together.
                </h1>
                <p className="text-slate-300 text-sm md:text-base leading-relaxed">
                  Ask academic or technical questions freely in{' '}
                  <span className="text-emerald-400 font-semibold">{selectedLanguage}</span>, English, or bilingual mode.
                  Get simple explanations, definitions, real examples, interactive vector diagrams, verified videos, and audio narration.
                  <span className="text-indigo-300 font-semibold"> PDF upload is optional!</span>
                </p>
              </div>

              {/* Quick Feature Highlights Cards */}
              <div className="grid grid-cols-2 gap-2.5 shrink-0">
                <div
                  onClick={() => setActiveTab('documents')}
                  className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/50 cursor-pointer transition-all"
                >
                  <FileText className="h-5 w-5 text-indigo-400 mb-1" />
                  <div className="text-xs font-bold text-white">RAG Document Chat</div>
                  <div className="text-[10px] text-slate-400">Page-indexed citations</div>
                </div>

                <div
                  onClick={() => setActiveTab('quizzes')}
                  className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-purple-500/50 cursor-pointer transition-all"
                >
                  <Award className="h-5 w-5 text-purple-400 mb-1" />
                  <div className="text-xs font-bold text-white">Interactive Quizzes</div>
                  <div className="text-[10px] text-slate-400">Instant test scoring</div>
                </div>

                <div
                  onClick={() => setActiveTab('flashcards')}
                  className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-amber-500/50 cursor-pointer transition-all"
                >
                  <Layers className="h-5 w-5 text-amber-400 mb-1" />
                  <div className="text-xs font-bold text-white">Study Flashcards</div>
                  <div className="text-[10px] text-slate-400">Spaced repetition recall</div>
                </div>

                <div
                  onClick={() => setActiveTab('community')}
                  className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/50 cursor-pointer transition-all"
                >
                  <Users className="h-5 w-5 text-emerald-400 mb-1" />
                  <div className="text-xs font-bold text-white">Find a Mentor</div>
                  <div className="text-[10px] text-slate-400">1-on-1 guidance</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 1: AI Learning Workspace (The Main Feature) */}
        {activeTab === 'workspace' && (
          <LearningWorkspace
            selectedLanguage={selectedLanguage}
            setSelectedLanguage={setSelectedLanguage}
            educationLevel={educationLevel}
            documents={documents}
            activeDocumentId={activeDocumentId}
            setActiveDocumentId={setActiveDocumentId}
            onOpenQuizModal={(t) => {
              setQuizTopic(t);
              setActiveTab('quizzes');
            }}
          />
        )}

        {/* Tab 2: PDF Document Library & RAG */}
        {activeTab === 'documents' && (
          <PDFManager
            documents={documents}
            setDocuments={setDocuments}
            activeDocumentId={activeDocumentId}
            setActiveDocumentId={setActiveDocumentId}
            onDocumentSelectForChat={(doc) => {
              setActiveDocumentId(doc.id);
              setActiveTab('workspace');
            }}
          />
        )}

        {/* Tab 3: Interactive Study Flashcards */}
        {activeTab === 'flashcards' && <FlashcardDeck />}

        {/* Tab 4: Practice Quizzes & Knowledge Tests */}
        {activeTab === 'quizzes' && <QuizView initialTopic={quizTopic} />}

        {/* Tab 5: Learner Progress & Recharts Analytics */}
        {activeTab === 'analytics' && (
          <ProgressDashboard
            onSelectRecommendedTopic={(rec) => {
              setActiveTab('workspace');
            }}
          />
        )}

        {/* Tab 6: Skill & Career Roadmaps */}
        {activeTab === 'roadmap' && <CareerRoadmap />}

        {/* Tab 7: Community, Mentors & Study Groups */}
        {activeTab === 'community' && <CommunityMentors />}
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800/80 bg-slate-950 py-8 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-white">LearnBridge AI</span>
            <span>—</span>
            <span>Learn Anything. Connect with Everyone. Grow Together.</span>
          </div>

          <div className="flex items-center space-x-6 text-slate-400">
            <span>Regional Language Learning (Telugu, Hindi, Tamil)</span>
            <span>•</span>
            <span>PyMuPDF RAG Citations</span>
            <span>•</span>
            <span>Privacy Preserving</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
