'use client';

import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import {
  TrendingUp,
  Award,
  Clock,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  BookMarked
} from 'lucide-react';
import { LearningStats } from '../types';
import { fetchProgressStats } from '../lib/api';

const PIE_COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ec4899'];

interface ProgressDashboardProps {
  onSelectRecommendedTopic?: (topic: string) => void;
}

export const ProgressDashboard: React.FC<ProgressDashboardProps> = ({ onSelectRecommendedTopic }) => {
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgressStats()
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading || !stats) {
    return <div className="p-16 text-center text-slate-400">Loading progress analytics...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Stat Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Learning Streak', value: `${stats.streak_days} Days`, icon: '🔥', desc: 'Consistent daily study' },
          { label: 'Questions Asked', value: stats.total_questions_asked, icon: '💬', desc: 'AI interactive queries' },
          { label: 'Avg Quiz Score', value: `${stats.average_quiz_score}%`, icon: '🏆', desc: 'Across all modules' },
          { label: 'Weekly Study Hours', value: `${stats.study_hours_this_week} hrs`, icon: '⏱️', desc: 'Active learning time' }
        ].map((item, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl space-y-1"
          >
            <div className="flex items-center justify-between text-2xl">
              <span>{item.icon}</span>
            </div>
            <div className="text-2xl font-extrabold text-white pt-1">{item.value}</div>
            <div className="text-xs font-semibold text-slate-300">{item.label}</div>
            <div className="text-[11px] text-slate-500">{item.desc}</div>
          </div>
        ))}
      </div>

      {/* Visual Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Study Time Bar Chart */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white">Weekly Study Activity</h3>
              <p className="text-xs text-slate-400">Hours spent studying concepts &amp; asking questions</p>
            </div>
            <div className="flex items-center space-x-1.5 text-xs text-emerald-400 font-semibold">
              <TrendingUp className="h-4 w-4" />
              <span>+18% vs last week</span>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.weekly_study_chart}>
                <XAxis dataKey="day" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} unit="h" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    color: '#fff',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="hours" fill="#6366f1" radius={[6, 6, 0, 0]} name="Study Hours" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Subject Breakdown Pie Chart */}
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Subject Mastery</h3>
            <p className="text-xs text-slate-400">Distribution across learning domains</p>
          </div>

          <div className="h-48 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.subject_distribution}
                  dataKey="percentage"
                  nameKey="subject"
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={4}
                >
                  {stats.subject_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    color: '#fff',
                    fontSize: '12px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-1.5 text-xs">
            {stats.subject_distribution.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-slate-300">
                <div className="flex items-center space-x-2">
                  <span
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ backgroundColor: PIE_COLORS[idx % PIE_COLORS.length] }}
                  />
                  <span>{item.subject}</span>
                </div>
                <span className="font-bold text-white">{item.percentage}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommendations: "What to Learn Next" */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/30 to-slate-900 border border-indigo-500/20 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white">Recommended: What to Learn Next</h3>
          </div>
          <span className="text-xs text-slate-400">Tailored by your quiz scores &amp; interests</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {stats.recommendations_what_to_learn_next.map((rec, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-indigo-500/60 transition-all space-y-2 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span className="text-indigo-400 font-semibold">{rec.category}</span>
                  <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                    {rec.difficulty}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white mt-1.5">{rec.title}</h4>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                <span className="text-xs text-slate-400 flex items-center space-x-1">
                  <Clock className="h-3.5 w-3.5" />
                  <span>{rec.estimated_mins} mins</span>
                </span>

                <button
                  onClick={() => onSelectRecommendedTopic && onSelectRecommendedTopic(rec.title)}
                  className="inline-flex items-center space-x-1 text-xs text-indigo-400 hover:text-indigo-300 font-bold"
                >
                  <span>Learn Now</span>
                  <ArrowRight className="h-3 w-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
