'use client';

import React from 'react';
import {
  Sparkles,
  BookOpen,
  FileText,
  BarChart3,
  Layers,
  Award,
  Users,
  Compass,
  Globe2,
  GraduationCap
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  selectedLanguage: string;
  setSelectedLanguage: (lang: string) => void;
  educationLevel: string;
  setEducationLevel: (level: string) => void;
  streakDays: number;
}

export const LANGUAGES = [
  'Telugu',
  'English',
  'English + Telugu',
  'Hindi',
  'Tamil',
  'Kannada',
  'Malayalam',
  'Marathi',
  'Bengali'
];

export const EDUCATION_LEVELS = [
  'College / Undergraduate',
  'High School (11th-12th)',
  'Competitive / GATE / Placements',
  'Beginner / General Learner'
];

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  selectedLanguage,
  setSelectedLanguage,
  educationLevel,
  setEducationLevel,
  streakDays
}) => {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800 text-white transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Tagline */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('workspace')}>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-emerald-400 p-0.5 shadow-lg shadow-indigo-500/20">
              <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Sparkles className="h-5 w-5 text-indigo-400 animate-pulse" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-300 bg-clip-text text-transparent">
                  LearnBridge<span className="text-emerald-400">.ai</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Tutor
                </span>
              </div>
              <p className="hidden md:block text-[11px] text-slate-400 font-medium">
                Learn Anything. Connect with Everyone. Grow Together.
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden lg:flex items-center space-x-1">
            {[
              { id: 'workspace', label: 'AI Workspace', icon: Sparkles },
              { id: 'documents', label: 'PDF Library', icon: FileText },
              { id: 'flashcards', label: 'Flashcards', icon: Layers },
              { id: 'quizzes', label: 'Quizzes', icon: Award },
              { id: 'analytics', label: 'Analytics', icon: BarChart3 },
              { id: 'roadmap', label: 'Roadmaps', icon: Compass },
              { id: 'community', label: 'Mentors', icon: Users }
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-500/25 ring-1 ring-white/20'
                      : 'text-slate-300 hover:text-white hover:bg-slate-900/80'
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Controls: Language Selector, Level, Streak */}
          <div className="flex items-center space-x-3">
            {/* Streak Badge */}
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold" title="Current Learning Streak">
              <span>🔥</span>
              <span>{streakDays}d Streak</span>
            </div>

            {/* Language Selector */}
            <div className="relative flex items-center">
              <Globe2 className="absolute left-2.5 h-3.5 w-3.5 text-indigo-400 pointer-events-none" />
              <select
                aria-label="Select Learning Language"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-slate-900 border border-slate-700 hover:border-indigo-500 text-xs font-medium text-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer transition-all"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang} value={lang} className="bg-slate-900 text-white">
                    {lang}
                  </option>
                ))}
              </select>
            </div>

            {/* Education Level */}
            <div className="relative hidden xl:flex items-center">
              <GraduationCap className="absolute left-2.5 h-3.5 w-3.5 text-emerald-400 pointer-events-none" />
              <select
                aria-label="Select Education Level"
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-slate-900 border border-slate-700 hover:border-emerald-500 text-xs font-medium text-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 cursor-pointer transition-all"
              >
                {EDUCATION_LEVELS.map((lvl) => (
                  <option key={lvl} value={lvl} className="bg-slate-900 text-white">
                    {lvl}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Nav Scrollable Strip */}
      <div className="lg:hidden flex overflow-x-auto space-x-1 py-2 px-4 border-t border-slate-800/80 bg-slate-950 scrollbar-none">
        {[
          { id: 'workspace', label: 'Workspace' },
          { id: 'documents', label: 'PDFs' },
          { id: 'flashcards', label: 'Flashcards' },
          { id: 'quizzes', label: 'Quizzes' },
          { id: 'analytics', label: 'Progress' },
          { id: 'roadmap', label: 'Roadmap' },
          { id: 'community', label: 'Mentors' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`whitespace-nowrap px-3 py-1 rounded-full text-xs font-semibold ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:bg-slate-900'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </header>
  );
};
