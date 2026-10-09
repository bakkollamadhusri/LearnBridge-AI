'use client';

import React, { useState, useEffect } from 'react';
import { Award, Check, AlertCircle, Sparkles, RotateCcw, X } from 'lucide-react';
import confetti from 'canvas-confetti';
import { PracticeQuestion } from '../types';
import { fetchQuiz, submitQuizAnswers } from '../lib/api';

interface QuizViewProps {
  initialTopic?: string;
  onClose?: () => void;
}

export const QuizView: React.FC<QuizViewProps> = ({ initialTopic = 'Machine Learning', onClose }) => {
  const [topic, setTopic] = useState(initialTopic);
  const [questions, setQuestions] = useState<PracticeQuestion[]>([]);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [quizResult, setQuizResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadQuiz = async (selectedTopic: string) => {
    setLoading(true);
    setSubmitted(false);
    setSelectedAnswers({});
    setQuizResult(null);
    try {
      const data = await fetchQuiz(selectedTopic);
      setQuestions(data);
    } catch {}
    setLoading(false);
  };

  useEffect(() => {
    loadQuiz(topic);
  }, [topic]);

  const handleSubmit = async () => {
    if (Object.keys(selectedAnswers).length < questions.length) {
      if (!confirm('You have unanswered questions. Are you sure you want to submit?')) return;
    }

    try {
      const res = await submitQuizAnswers(topic, selectedAnswers);
      setQuizResult(res);
      setSubmitted(true);

      if (res.score_percentage >= 70) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
    } catch (err: any) {
      alert('Error submitting quiz: ' + err.message);
    }
  };

  return (
    <div className="space-y-6">
      {/* Quiz Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/20 shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
            <Award className="h-4 w-4" />
            <span>Interactive Assessment</span>
          </div>
          <h2 className="text-2xl font-bold text-white mt-1">Practice Quiz &amp; Knowledge Test</h2>
          <p className="text-slate-300 text-sm mt-1">
            Multiple-choice problem tests with detailed conceptual rationale and performance scores.
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
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-16 text-center text-slate-400">Loading quiz questions...</div>
      ) : questions.length === 0 ? (
        <div className="p-16 text-center text-slate-400">No questions found.</div>
      ) : (
        <div className="space-y-6 max-w-3xl mx-auto">
          {/* Result Card if Submitted */}
          {submitted && quizResult && (
            <div className="p-6 rounded-2xl bg-gradient-to-b from-indigo-950/40 to-slate-900 border border-indigo-500/40 space-y-3 text-center">
              <span className="text-4xl font-extrabold bg-gradient-to-r from-emerald-400 to-indigo-300 bg-clip-text text-transparent">
                {quizResult.score_percentage}%
              </span>
              <p className="text-white text-sm font-semibold">
                You scored {quizResult.correct_count} out of {quizResult.total_questions} questions correctly!
              </p>
              <p className="text-xs text-indigo-200">{quizResult.feedback}</p>
              <button
                onClick={() => loadQuiz(topic)}
                className="mt-2 inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all"
              >
                <RotateCcw className="h-3.5 w-3.5" />
                <span>Retry Quiz</span>
              </button>
            </div>
          )}

          {/* Question List */}
          <div className="space-y-5">
            {questions.map((q, idx) => {
              const selected = selectedAnswers[idx];
              const isCorrect = selected === q.correct_answer;

              return (
                <div
                  key={idx}
                  className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <span className="text-xs font-bold uppercase text-indigo-400">
                      Question {idx + 1}
                    </span>
                    {submitted && (
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          isCorrect
                            ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                            : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        }`}
                      >
                        {isCorrect ? 'Correct (+1)' : 'Incorrect (0)'}
                      </span>
                    )}
                  </div>

                  <h3 className="text-sm font-bold text-white">{q.question}</h3>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                    {q.options.map((opt, oIdx) => {
                      const isChosen = selected === oIdx;
                      let btnStyle = 'bg-slate-950/80 border-slate-800 text-slate-300 hover:border-slate-700';

                      if (submitted) {
                        if (oIdx === q.correct_answer) {
                          btnStyle = 'bg-emerald-950/80 border-emerald-500 text-emerald-200 font-bold';
                        } else if (isChosen) {
                          btnStyle = 'bg-rose-950/80 border-rose-500 text-rose-200';
                        }
                      } else if (isChosen) {
                        btnStyle = 'bg-indigo-950 border-indigo-500 text-white font-bold ring-1 ring-indigo-500';
                      }

                      return (
                        <button
                          key={oIdx}
                          disabled={submitted}
                          onClick={() => setSelectedAnswers((prev) => ({ ...prev, [idx]: oIdx }))}
                          className={`p-3 rounded-xl border text-left text-xs transition-all flex items-center justify-between ${btnStyle}`}
                        >
                          <span>{opt}</span>
                          {submitted && oIdx === q.correct_answer && (
                            <Check className="h-4 w-4 text-emerald-400 shrink-0 ml-1" />
                          )}
                        </button>
                      );
                    })}
                  </div>

                  {submitted && (
                    <div className="p-3 rounded-xl bg-slate-950 text-xs text-slate-300 border border-slate-800/80 leading-relaxed">
                      <span className="font-bold text-indigo-400">Explanation: </span>
                      {q.explanation}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {!submitted && (
            <div className="text-center pt-2">
              <button
                onClick={handleSubmit}
                className="px-8 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-500/25 transition-all"
              >
                Submit Quiz &amp; View Score
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
