'use client';

import React, { useState, useEffect } from 'react';
import { Compass, CheckCircle2, Clock, Sparkles, BookOpen, ChevronRight } from 'lucide-react';
import { fetchRoadmap } from '../lib/api';

export const CareerRoadmap: React.FC = () => {
  const [track, setTrack] = useState('Full-Stack AI Developer');
  const [roadmapData, setRoadmapData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchRoadmap(track)
      .then((data) => {
        setRoadmapData(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [track]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/20 shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
            <Compass className="h-4 w-4" />
            <span>Career Pathways</span>
          </div>
          <h2 className="text-2xl font-bold text-white mt-1">Skill &amp; Career Learning Roadmaps</h2>
          <p className="text-slate-300 text-sm mt-1">
            Step-by-step curriculum with estimated completion times, milestones, and technical interview preparation.
          </p>
        </div>

        {/* Track Selector */}
        <div className="flex items-center space-x-2">
          {['Full-Stack AI Developer', 'Machine Learning Engineer', 'Web Developer'].map((t) => (
            <button
              key={t}
              onClick={() => setTrack(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                track === t
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {loading || !roadmapData ? (
        <div className="p-16 text-center text-slate-400">Loading career curriculum...</div>
      ) : (
        <div className="space-y-4 max-w-4xl mx-auto">
          <div className="flex items-center justify-between text-xs text-slate-400 px-2">
            <span className="font-semibold text-white text-sm">{roadmapData.career_track}</span>
            <span>Total Estimated Duration: {roadmapData.total_estimated_weeks} Weeks</span>
          </div>

          <div className="relative border-l-2 border-indigo-500/30 ml-4 md:ml-6 space-y-6 py-2">
            {roadmapData.phases.map((phase: any, idx: number) => (
              <div key={idx} className="relative pl-6 md:pl-8">
                {/* Node circle */}
                <div className="absolute -left-[17px] top-1.5 h-8 w-8 rounded-full bg-slate-900 border-2 border-indigo-500 flex items-center justify-center text-indigo-400 font-bold text-xs shadow-md">
                  {phase.step}
                </div>

                <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40 transition-all space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20">
                        {phase.phase}
                      </span>
                      <h4 className="text-base font-bold text-white mt-1">{phase.title}</h4>
                    </div>

                    <span className="flex items-center space-x-1 text-xs text-slate-400">
                      <Clock className="h-3.5 w-3.5 text-slate-500" />
                      <span>{phase.weeks} Weeks</span>
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {phase.skills.map((skill: string, sIdx: number) => (
                      <span
                        key={sIdx}
                        className="px-2.5 py-1 rounded-lg bg-slate-950 text-slate-300 text-xs border border-slate-800"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
