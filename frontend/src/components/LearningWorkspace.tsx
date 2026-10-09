'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Sparkles,
  FileText,
  Volume2,
  VolumeX,
  Play,
  Pause,
  RotateCcw,
  BookOpen,
  Lightbulb,
  Cpu,
  Video,
  CheckCircle,
  HelpCircle,
  ArrowRight,
  ExternalLink,
  ChevronDown,
  Layers,
  FileCheck,
  Languages,
  Check,
  AlertTriangle
} from 'lucide-react';
import {
  LearningResponse,
  DocumentMetadata,
  SourceMode,
  PracticeQuestion
} from '../types';
import { askQuestion } from '../lib/api';

interface LearningWorkspaceProps {
  selectedLanguage: string;
  setSelectedLanguage: (lang: string) => void;
  educationLevel: string;
  documents: DocumentMetadata[];
  activeDocumentId: string | null;
  setActiveDocumentId: (id: string | null) => void;
  onOpenQuizModal?: (topic: string) => void;
}

export const LearningWorkspace: React.FC<LearningWorkspaceProps> = ({
  selectedLanguage,
  setSelectedLanguage,
  educationLevel,
  documents,
  activeDocumentId,
  setActiveDocumentId,
  onOpenQuizModal
}) => {
  const [questionInput, setQuestionInput] = useState('');
  const [sourceMode, setSourceMode] = useState<SourceMode>('general_ai');
  const [loading, setLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState<LearningResponse | null>(null);
  const [conversationHistory, setConversationHistory] = useState<Array<{ role: string; content: string }>>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Audio / Speech State
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [isPausedAudio, setIsPausedAudio] = useState(false);
  const speechUtteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  // Quiz state for inside response
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [showQuizRationale, setShowQuizRationale] = useState<Record<number, boolean>>({});

  const activeDoc = documents.find((d) => d.id === activeDocumentId);

  // Sync sourceMode when activeDocumentId changes
  useEffect(() => {
    if (activeDocumentId) {
      if (sourceMode === 'general_ai') {
        setSourceMode('pdf_and_ai');
      }
    } else {
      setSourceMode('general_ai');
    }
  }, [activeDocumentId]);

  // Audio Speech synthesis handler
  const handlePlayAudio = (text: string) => {
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support Web Speech synthesis.');
      return;
    }

    if (isPlayingAudio && !isPausedAudio) {
      window.speechSynthesis.pause();
      setIsPausedAudio(true);
      return;
    }

    if (isPausedAudio) {
      window.speechSynthesis.resume();
      setIsPausedAudio(false);
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    speechUtteranceRef.current = utterance;

    // Pick appropriate voice if available
    const voices = window.speechSynthesis.getVoices();
    if (selectedLanguage.toLowerCase().includes('telugu')) {
      const teVoice = voices.find((v) => v.lang.includes('te') || v.lang.includes('te-IN'));
      if (teVoice) utterance.voice = teVoice;
    } else if (selectedLanguage.toLowerCase().includes('hindi')) {
      const hiVoice = voices.find((v) => v.lang.includes('hi') || v.lang.includes('hi-IN'));
      if (hiVoice) utterance.voice = hiVoice;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      setIsPlayingAudio(true);
      setIsPausedAudio(false);
    };

    utterance.onend = () => {
      setIsPlayingAudio(false);
      setIsPausedAudio(false);
    };

    utterance.onerror = () => {
      setIsPlayingAudio(false);
      setIsPausedAudio(false);
    };

    window.speechSynthesis.speak(utterance);
  };

  const handleStopAudio = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlayingAudio(false);
    setIsPausedAudio(false);
  };

  const handleAsk = async (queryText?: string) => {
    const q = (queryText || questionInput).trim();
    if (!q) return;

    setLoading(true);
    setErrorMsg(null);
    handleStopAudio();
    setQuizAnswers({});
    setShowQuizRationale({});

    try {
      const response = await askQuestion({
        question: q,
        document_id: activeDocumentId,
        source_mode: activeDocumentId ? sourceMode : 'general_ai',
        language: selectedLanguage,
        education_level: educationLevel,
        conversation_history: conversationHistory
      });

      setCurrentResponse(response);
      setConversationHistory((prev) => [
        ...prev,
        { role: 'user', content: q },
        { role: 'assistant', content: response.simple_explanation }
      ]);
      setQuestionInput('');
    } catch (err: any) {
      setErrorMsg(err.message || 'Error communicating with AI learning tutor.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (actionType: string) => {
    const currentTopic = currentResponse?.question || questionInput || 'Machine Learning';
    switch (actionType) {
      case 'simple':
        handleAsk(`Explain ${currentTopic} in very simple words for a beginner`);
        break;
      case 'step_by_step':
        handleAsk(`Explain how ${currentTopic} works step by step`);
        break;
      case 'example':
        handleAsk(`Give practical, real-world examples of ${currentTopic}`);
        break;
      case 'language':
        handleAsk(`Explain ${currentTopic} in ${selectedLanguage}`);
        break;
      case 'diagram':
        handleAsk(`Show diagram and visual breakdown of ${currentTopic}`);
        break;
      case 'quiz':
        if (onOpenQuizModal) {
          onOpenQuizModal(currentTopic);
        } else {
          handleAsk(`Generate a practice quiz on ${currentTopic}`);
        }
        break;
      case 'summarize':
        handleAsk(`Summarize the key takeaways and formulas for ${currentTopic}`);
        break;
      default:
        break;
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Prompt Controls Card */}
      <div className="rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 p-5 md:p-6 border border-slate-800 shadow-2xl">
        {/* Source Mode & Document Selector Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-slate-800/80">
          {/* Source Mode Tabs */}
          <div className="flex items-center space-x-1.5 p-1 rounded-xl bg-slate-950 border border-slate-800 text-xs font-semibold">
            {[
              {
                id: 'pdf_and_ai' as SourceMode,
                label: 'PDF + AI Knowledge',
                desc: 'Uses PDF first, augments with AI',
                disabled: !activeDoc
              },
              {
                id: 'pdf_only' as SourceMode,
                label: 'PDF Only (Strict)',
                desc: 'Answers strictly from document only',
                disabled: !activeDoc
              },
              {
                id: 'general_ai' as SourceMode,
                label: 'General AI',
                desc: 'No PDF required',
                disabled: false
              }
            ].map((m) => (
              <button
                key={m.id}
                onClick={() => setSourceMode(m.id)}
                disabled={m.disabled}
                title={m.desc}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  sourceMode === m.id
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-sm'
                    : m.disabled
                    ? 'text-slate-600 cursor-not-allowed'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>

          {/* Active Document Indicator or Selector */}
          <div className="flex items-center space-x-2 text-xs">
            {activeDoc ? (
              <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-indigo-950/60 border border-indigo-500/40 text-indigo-300">
                <FileCheck className="h-4 w-4 text-emerald-400" />
                <span className="font-semibold max-w-[180px] md:max-w-[260px] truncate">
                  {activeDoc.filename} ({activeDoc.total_pages}p)
                </span>
                <button
                  onClick={() => setActiveDocumentId(null)}
                  className="text-slate-400 hover:text-rose-400 ml-1 text-xs"
                  title="Remove document context"
                >
                  ✕
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2 text-slate-400 bg-slate-950/80 px-3 py-1.5 rounded-lg border border-slate-800/80">
                <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                <span>General AI Mode (No PDF required)</span>
              </div>
            )}
          </div>
        </div>

        {/* Question Input Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleAsk();
          }}
          className="relative"
        >
          <div className="relative flex items-center">
            <textarea
              rows={2}
              value={questionInput}
              onChange={(e) => setQuestionInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleAsk();
                }
              }}
              placeholder={`Ask anything you want to learn, in your preferred language (${selectedLanguage})...`}
              className="w-full bg-slate-950/90 border border-slate-700/80 hover:border-slate-600 focus:border-indigo-500 rounded-xl py-3.5 pl-4 pr-14 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40 placeholder-slate-500 transition-all resize-none"
            />
            <button
              type="submit"
              disabled={loading || !questionInput.trim()}
              className="absolute right-2.5 bottom-3.5 p-2.5 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-40 text-white shadow-md shadow-indigo-500/25 transition-all"
            >
              <Send className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </form>

        {/* Quick Sample Prompts */}
        <div className="flex flex-wrap items-center gap-2 mt-3 pt-2 text-xs">
          <span className="text-slate-500 font-medium">Try asking:</span>
          {[
            'Explain Machine Learning in Telugu',
            'What is a PN Junction Diode?',
            'How does Photosynthesis work?',
            'Explain Neural Networks step by step',
            'Water cycle with real world examples'
          ].map((sample) => (
            <button
              key={sample}
              onClick={() => handleAsk(sample)}
              className="px-2.5 py-1 rounded-full bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 text-slate-300 hover:text-white transition-colors"
            >
              {sample}
            </button>
          ))}
        </div>
      </div>

      {/* Error Message Alert */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center space-x-3">
          <AlertTriangle className="h-5 w-5 shrink-0 text-rose-400" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* AI Smart Answer Container */}
      {loading && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center">
          <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 animate-bounce mb-3">
            <Sparkles className="h-7 w-7" />
          </div>
          <h3 className="text-lg font-bold text-white">Synthesizing Pedagogical Explanation...</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-md mx-auto">
            Structuring simple definitions, step-by-step logic, diagrams, regional translations, and citations...
          </p>
        </div>
      )}

      {currentResponse && !loading && (
        <div className="space-y-6">
          {/* Quick Actions Toolbar */}
          <div className="flex flex-wrap items-center gap-1.5 p-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold overflow-x-auto">
            <span className="text-slate-500 px-2 uppercase text-[10px] tracking-wider">Quick Actions:</span>
            <button
              onClick={() => handleQuickAction('simple')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors flex items-center space-x-1"
            >
              <span>🧸 Simple Words</span>
            </button>
            <button
              onClick={() => handleQuickAction('step_by_step')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors flex items-center space-x-1"
            >
              <span>🪜 Step by Step</span>
            </button>
            <button
              onClick={() => handleQuickAction('example')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors flex items-center space-x-1"
            >
              <span>💡 Real Example</span>
            </button>
            <button
              onClick={() => handleQuickAction('language')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 transition-colors flex items-center space-x-1"
            >
              <span>🌐 In {selectedLanguage}</span>
            </button>
            <button
              onClick={() => handleQuickAction('diagram')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-300 transition-colors flex items-center space-x-1"
            >
              <span>📊 Diagram</span>
            </button>
            <button
              onClick={() => handlePlayAudio(currentResponse.audio_text)}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 transition-colors flex items-center space-x-1"
            >
              <span>🔊 Listen</span>
            </button>
            <button
              onClick={() => handleQuickAction('quiz')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-purple-300 transition-colors flex items-center space-x-1"
            >
              <span>🏆 Quiz</span>
            </button>
            <button
              onClick={() => handleQuickAction('summarize')}
              className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors flex items-center space-x-1"
            >
              <span>📝 Summarize</span>
            </button>
          </div>

          {/* Main Answer Header & Mode Badge */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm p-6 shadow-xl space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/80">
              <div className="flex items-center space-x-2.5">
                <div className="h-8 w-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                  <Sparkles className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white capitalize">
                    {currentResponse.question}
                  </h3>
                  <div className="flex items-center space-x-2 text-xs text-slate-400">
                    <span className="font-semibold text-indigo-400">{currentResponse.language}</span>
                    <span>•</span>
                    <span className="capitalize">{currentResponse.source_mode.replace(/_/g, ' ')}</span>
                  </div>
                </div>
              </div>

              {/* TTS Listen Button */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handlePlayAudio(currentResponse.audio_text)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                    isPlayingAudio
                      ? 'bg-amber-500 text-slate-950 font-bold animate-pulse'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                  }`}
                >
                  {isPlayingAudio ? (
                    <>
                      <Pause className="h-3.5 w-3.5" />
                      <span>{isPausedAudio ? 'Resume' : 'Pause Audio'}</span>
                    </>
                  ) : (
                    <>
                      <Volume2 className="h-3.5 w-3.5 text-amber-400" />
                      <span>Listen to Explanation</span>
                    </>
                  )}
                </button>
                {isPlayingAudio && (
                  <button
                    onClick={handleStopAudio}
                    title="Stop audio playback"
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs"
                  >
                    <VolumeX className="h-3.5 w-3.5" />
                  </button>
                )}
              </div>
            </div>

            {/* Section 1: Simple Explanation */}
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
                <BookOpen className="h-3.5 w-3.5" />
                <span>1. Simple Explanation</span>
              </div>
              <div className="text-slate-100 text-sm md:text-base leading-relaxed whitespace-pre-line bg-slate-950/40 p-4 rounded-xl border border-slate-800/60 font-sans">
                {currentResponse.simple_explanation}
              </div>
            </div>

            {/* Section 2: Definition */}
            {currentResponse.definition && (
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                  <FileText className="h-3.5 w-3.5" />
                  <span>2. Definition</span>
                </div>
                <div className="text-slate-200 text-sm leading-relaxed p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-500/20">
                  {currentResponse.definition}
                </div>
              </div>
            )}

            {/* Section 3: How It Works */}
            {currentResponse.how_it_works && (
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-purple-400 text-xs font-bold uppercase tracking-wider">
                  <Cpu className="h-3.5 w-3.5" />
                  <span>3. How It Works (Step-by-Step)</span>
                </div>
                {Array.isArray(currentResponse.how_it_works) ? (
                  <div className="grid grid-cols-1 gap-2">
                    {currentResponse.how_it_works.map((step, idx) => (
                      <div
                        key={idx}
                        className="flex items-start space-x-3 p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-xs md:text-sm text-slate-300"
                      >
                        <span className="h-5 w-5 rounded-full bg-purple-500/20 text-purple-300 font-bold text-xs flex items-center justify-center shrink-0">
                          {idx + 1}
                        </span>
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-slate-300 text-sm p-3 rounded-lg bg-slate-950/60 border border-slate-800">
                    {currentResponse.how_it_works}
                  </div>
                )}
              </div>
            )}

            {/* Section 4: Real-world Example */}
            {currentResponse.example && (
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                  <Lightbulb className="h-3.5 w-3.5" />
                  <span>4. Practical Real-Life Example</span>
                </div>
                <div className="text-slate-200 text-sm leading-relaxed p-4 rounded-xl bg-amber-950/20 border border-amber-500/20 whitespace-pre-line">
                  {currentResponse.example}
                </div>
              </div>
            )}

            {/* Section 5: Educational Visual / Interactive SVG Diagram */}
            {currentResponse.visual_diagram && (
              <div className="space-y-3 pt-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-sky-400 text-xs font-bold uppercase tracking-wider">
                    <Layers className="h-3.5 w-3.5" />
                    <span>5. Visual Explanation &amp; Interactive Diagram</span>
                  </div>
                  <span className="text-[11px] font-semibold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                    Vector Graphic
                  </span>
                </div>

                <div className="rounded-xl overflow-hidden border border-slate-700 bg-slate-950 p-3 shadow-inner">
                  {currentResponse.visual_diagram.svg_content ? (
                    <div
                      dangerouslySetInnerHTML={{
                        __html: currentResponse.visual_diagram.svg_content
                      }}
                      className="w-full flex justify-center"
                    />
                  ) : null}
                  <div className="p-3 bg-slate-900/60 border-t border-slate-800 mt-2 rounded-lg">
                    <p className="text-xs text-slate-300 font-medium">
                      {currentResponse.visual_diagram.description}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Section 6: Watch and Listen (Educational Videos) */}
            {currentResponse.videos && currentResponse.videos.length > 0 && (
              <div className="space-y-3 pt-2">
                <div className="flex items-center space-x-2 text-rose-400 text-xs font-bold uppercase tracking-wider">
                  <Video className="h-3.5 w-3.5" />
                  <span>6. Watch &amp; Listen — Educational Video Tutorials</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentResponse.videos.map((vid, vIdx) => (
                    <div
                      key={vIdx}
                      className="rounded-xl border border-slate-800 bg-slate-950 overflow-hidden hover:border-slate-700 transition-all flex flex-col justify-between"
                    >
                      {vid.embed_url ? (
                        <div className="relative pt-[56.25%] w-full bg-slate-900">
                          <iframe
                            src={vid.embed_url}
                            title={vid.title}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="absolute top-0 left-0 w-full h-full border-0"
                          />
                        </div>
                      ) : (
                        <a
                          href={vid.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="relative block group"
                        >
                          <img
                            src={vid.thumbnail_url}
                            alt={vid.title}
                            className="w-full h-40 object-cover group-hover:opacity-90 transition-opacity"
                          />
                          <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/80 text-[11px] font-bold text-white">
                            {vid.duration}
                          </div>
                        </a>
                      )}

                      <div className="p-3.5 space-y-2">
                        <div className="flex items-center justify-between text-[11px] text-slate-400">
                          <span className="font-semibold text-indigo-400">{vid.channel}</span>
                          <span className="px-1.5 py-0.5 rounded bg-slate-800 font-bold text-slate-300">
                            {vid.language}
                          </span>
                        </div>
                        <h5 className="text-xs font-bold text-white line-clamp-2">
                          {vid.title}
                        </h5>
                        <p className="text-[11px] text-slate-400 line-clamp-2">
                          {vid.description}
                        </p>
                        <a
                          href={vid.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-1 text-xs text-indigo-400 hover:text-indigo-300 font-semibold pt-1"
                        >
                          <span>Open on YouTube</span>
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Section 7: Key Points */}
            {currentResponse.key_points && currentResponse.key_points.length > 0 && (
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold uppercase tracking-wider">
                  <CheckCircle className="h-3.5 w-3.5" />
                  <span>7. Key Points Summary</span>
                </div>
                <ul className="space-y-1.5 text-xs md:text-sm text-slate-300">
                  {currentResponse.key_points.map((pt, pIdx) => (
                    <li key={pIdx} className="flex items-start space-x-2">
                      <span className="text-cyan-400 font-bold">•</span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Section 8: Interactive Practice Questions / Quiz */}
            {currentResponse.practice_questions && currentResponse.practice_questions.length > 0 && (
              <div className="space-y-3 pt-2">
                <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                  <HelpCircle className="h-3.5 w-3.5" />
                  <span>8. Practice Questions (Test Your Understanding)</span>
                </div>

                <div className="space-y-4">
                  {currentResponse.practice_questions.map((pq, qIdx) => {
                    const selectedOpt = quizAnswers[qIdx];
                    const isAnswered = selectedOpt !== undefined;
                    const isCorrect = selectedOpt === pq.correct_answer;

                    return (
                      <div
                        key={qIdx}
                        className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3"
                      >
                        <p className="text-sm font-semibold text-white">
                          Q{qIdx + 1}: {pq.question}
                        </p>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {pq.options.map((opt, oIdx) => {
                            let btnStyle = 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-850';
                            if (isAnswered) {
                              if (oIdx === pq.correct_answer) {
                                btnStyle = 'bg-emerald-950/60 border-emerald-500 text-emerald-200 font-bold';
                              } else if (selectedOpt === oIdx) {
                                btnStyle = 'bg-rose-950/60 border-rose-500 text-rose-200';
                              }
                            }

                            return (
                              <button
                                key={oIdx}
                                disabled={isAnswered}
                                onClick={() => {
                                  setQuizAnswers((prev) => ({ ...prev, [qIdx]: oIdx }));
                                  setShowQuizRationale((prev) => ({ ...prev, [qIdx]: true }));
                                }}
                                className={`p-2.5 rounded-lg border text-left text-xs transition-all flex items-center justify-between ${btnStyle}`}
                              >
                                <span>{opt}</span>
                                {isAnswered && oIdx === pq.correct_answer && (
                                  <Check className="h-3.5 w-3.5 text-emerald-400 shrink-0 ml-1" />
                                )}
                              </button>
                            );
                          })}
                        </div>

                        {showQuizRationale[qIdx] && (
                          <div
                            className={`p-3 rounded-lg text-xs leading-relaxed ${
                              isCorrect
                                ? 'bg-emerald-950/30 border border-emerald-500/20 text-emerald-300'
                                : 'bg-slate-900 border border-slate-800 text-slate-300'
                            }`}
                          >
                            <span className="font-bold">{isCorrect ? '✅ Correct! ' : '💡 Explanation: '}</span>
                            {pq.explanation}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* RAG Citations Accordion (When in PDF mode) */}
            {currentResponse.citations && currentResponse.citations.length > 0 && (
              <div className="pt-2 border-t border-slate-800/80">
                <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-2">
                  <FileCheck className="h-3.5 w-3.5" />
                  <span>Supporting PDF Citations &amp; Evidence ({currentResponse.citations.length})</span>
                </div>

                <div className="grid grid-cols-1 gap-2">
                  {currentResponse.citations.map((cit, cIdx) => (
                    <div
                      key={cIdx}
                      className="p-3.5 rounded-xl bg-indigo-950/20 border border-indigo-500/20 space-y-1"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-indigo-300">
                          📄 {cit.filename} — Page {cit.page_number}
                        </span>
                        <span className="text-[11px] font-semibold text-emerald-400">
                          Relevance Match: {(cit.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 italic bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                        "{cit.text_snippet}"
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Section 9: Suggested Follow-up Questions */}
            {currentResponse.follow_up_questions && currentResponse.follow_up_questions.length > 0 && (
              <div className="pt-2 border-t border-slate-800/80">
                <span className="text-slate-400 text-xs font-semibold block mb-2">
                  Explore further (Suggested follow-ups):
                </span>
                <div className="flex flex-wrap gap-2">
                  {currentResponse.follow_up_questions.map((fq, fIdx) => (
                    <button
                      key={fIdx}
                      onClick={() => handleAsk(fq)}
                      className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-750 border border-slate-700/60 hover:border-indigo-500 text-slate-200 text-xs font-medium flex items-center space-x-1.5 transition-all"
                    >
                      <span>{fq}</span>
                      <ArrowRight className="h-3 w-3 text-indigo-400" />
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
