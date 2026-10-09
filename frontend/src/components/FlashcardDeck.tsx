'use client';

import React, { useState, useEffect } from 'react';
import { Layers, RotateCcw, Check, Sparkles, ChevronLeft, ChevronRight } from 'lucide-react';
import { Flashcard } from '../types';
import { fetchFlashcards } from '../lib/api';

export const FlashcardDeck: React.FC = () => {
  const [topic, setTopic] = useState('Machine Learning');
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(false);
  const [masteredIds, setMasteredIds] = useState<Set<string>>(new Set());

  const loadCards = async (selectedTopic: string) => {
    setLoading(true);
    setIsFlipped(false);
    setCurrentIndex(0);
    try {
      const data = await fetchFlashcards(selectedTopic);
      setCards(data);
    } catch {}
    setLoading(false);
  };

  useEffect(() => {
    loadCards(topic);
  }, [topic]);

  const currentCard = cards[currentIndex];

  const toggleMastered = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setMasteredIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-purple-950/40 to-slate-900 border border-purple-500/20">
        <div>
          <div className="flex items-center space-x-2 text-purple-400 font-semibold text-xs tracking-wider uppercase">
            <Layers className="h-4 w-4" />
            <span>Interactive Study Materials</span>
          </div>
          <h2 className="text-2xl font-bold text-white mt-1">Smart AI Flashcards Deck</h2>
          <p className="text-slate-300 text-sm mt-1">
            Active recall and spaced repetition deck for mastering key definitions, equations, and rules.
          </p>
        </div>

        {/* Topic Selector */}
        <div className="flex items-center space-x-2">
          {['Machine Learning', 'P-N Junction', 'Photosynthesis', 'Python'].map((t) => (
            <button
              key={t}
              onClick={() => setTopic(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                topic === t
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-16 text-center text-slate-400">Loading flashcards deck...</div>
      ) : cards.length === 0 ? (
        <div className="p-16 text-center text-slate-400">No cards available for this topic.</div>
      ) : (
        <div className="max-w-xl mx-auto space-y-4">
          {/* Progress Strip */}
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>
              Card {currentIndex + 1} of {cards.length}
            </span>
            <span className="text-emerald-400 font-bold">
              {masteredIds.size} Mastered
            </span>
          </div>

          {/* Flashcard 3D Card */}
          <div
            onClick={() => setIsFlipped(!isFlipped)}
            className="relative h-72 w-full rounded-2xl border border-slate-700/80 bg-gradient-to-b from-slate-900 to-slate-950 p-6 flex flex-col justify-between cursor-pointer select-none shadow-2xl hover:border-purple-500/60 transition-all transform hover:-translate-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-bold">
                {currentCard.category}
              </span>

              <button
                onClick={(e) => toggleMastered(currentCard.id, e)}
                className={`flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-bold transition-all ${
                  masteredIds.has(currentCard.id)
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'bg-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Check className="h-3.5 w-3.5" />
                <span>{masteredIds.has(currentCard.id) ? 'Mastered' : 'Mark Learned'}</span>
              </button>
            </div>

            {/* Content Front / Back */}
            <div className="text-center px-4 my-auto">
              <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-2">
                {isFlipped ? '💡 Answer / Explanation' : '❓ Question (Click to reveal)'}
              </span>
              <p
                className={`text-base md:text-lg font-bold leading-relaxed ${
                  isFlipped ? 'text-emerald-300 font-medium text-base' : 'text-white'
                }`}
              >
                {isFlipped ? currentCard.answer : currentCard.question}
              </p>
            </div>

            <div className="flex items-center justify-center space-x-2 text-xs text-slate-500">
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Click anywhere to flip card</span>
            </div>
          </div>

          {/* Nav Controls */}
          <div className="flex items-center justify-between pt-2">
            <button
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex((prev) => (prev > 0 ? prev - 1 : cards.length - 1));
              }}
              className="flex items-center space-x-1 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200 text-xs font-bold transition-all"
            >
              <ChevronLeft className="h-4 w-4" />
              <span>Previous</span>
            </button>

            <button
              onClick={() => setIsFlipped(!isFlipped)}
              className="px-4 py-2 rounded-xl bg-purple-600/20 border border-purple-500/30 text-purple-300 hover:bg-purple-600/30 text-xs font-bold transition-all"
            >
              Flip Card
            </button>

            <button
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex((prev) => (prev < cards.length - 1 ? prev + 1 : 0));
              }}
              className="flex items-center space-x-1 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200 text-xs font-bold transition-all"
            >
              <span>Next</span>
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
