'use client';

import React, { useState, useEffect } from 'react';
import { Users, Star, Calendar, Clock, MessageSquare, CheckCircle, Globe2, X } from 'lucide-react';
import { MentorProfile, StudyGroup } from '../types';
import { fetchMentors, fetchStudyGroups, bookMentorSession } from '../lib/api';

export const CommunityMentors: React.FC = () => {
  const [mentors, setMentors] = useState<MentorProfile[]>([]);
  const [groups, setGroups] = useState<StudyGroup[]>([]);
  const [selectedMentor, setSelectedMentor] = useState<MentorProfile | null>(null);
  const [bookingSuccess, setBookingSuccess] = useState<string | null>(null);

  // Form inputs
  const [learnerName, setLearnerName] = useState('');
  const [learnerEmail, setLearnerEmail] = useState('');
  const [prefDate, setPrefDate] = useState('2026-10-15');
  const [prefTime, setPrefTime] = useState('6:00 PM IST');
  const [topicDesc, setTopicDesc] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchMentors().then(setMentors);
    fetchStudyGroups().then(setGroups);
  }, []);

  const handleBook = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedMentor) return;

    setSubmitting(true);
    try {
      const res = await bookMentorSession({
        mentor_id: selectedMentor.id,
        learner_name: learnerName,
        learner_email: learnerEmail,
        preferred_date: prefDate,
        preferred_time: prefTime,
        topic_description: topicDesc
      });

      setBookingSuccess(res.message);
      setTimeout(() => {
        setBookingSuccess(null);
        setSelectedMentor(null);
        setLearnerName('');
        setLearnerEmail('');
        setTopicDesc('');
      }, 3500);
    } catch (err: any) {
      alert('Error booking session: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/20 shadow-xl">
        <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
          <Users className="h-4 w-4" />
          <span>Community &amp; Mentorship</span>
        </div>
        <h2 className="text-2xl font-bold text-white mt-1">Connect with Mentors &amp; Study Groups</h2>
        <p className="text-slate-300 text-sm mt-1">
          Learn directly from professors, industry engineers, and regional language peer circles.
        </p>
      </div>

      {/* Verified Mentors Section */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center space-x-2">
          <span>Verified Mentors</span>
          <span className="text-xs text-indigo-400 font-normal">
            (1-on-1 Guidance &amp; Code Review)
          </span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {mentors.map((m) => (
            <div
              key={m.id}
              className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="flex items-start space-x-4">
                <img
                  src={m.avatar_url}
                  alt={m.name}
                  className="h-14 w-14 rounded-2xl object-cover border border-slate-700 shrink-0"
                />
                <div className="min-w-0">
                  <div className="flex items-center space-x-2">
                    <h4 className="text-base font-bold text-white">{m.name}</h4>
                    <div className="flex items-center text-amber-400 text-xs font-bold">
                      <Star className="h-3.5 w-3.5 fill-amber-400 mr-0.5" />
                      <span>{m.rating}</span>
                    </div>
                  </div>
                  <p className="text-xs text-indigo-300 font-semibold">{m.title}</p>
                  <p className="text-[11px] text-slate-400">{m.institution_or_company}</p>

                  <div className="flex flex-wrap gap-1 mt-2">
                    {m.languages.map((l, lIdx) => (
                      <span
                        key={lIdx}
                        className="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[10px] font-semibold"
                      >
                        {l}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex flex-wrap gap-1.5">
                  {m.specialties.map((s, sIdx) => (
                    <span
                      key={sIdx}
                      className="px-2 py-0.5 rounded-md bg-slate-950 text-slate-300 text-[11px] border border-slate-800"
                    >
                      {s}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-slate-800">
                  <span className="text-xs text-emerald-400 font-bold">
                    Free Student Mentorship
                  </span>
                  <button
                    onClick={() => setSelectedMentor(m)}
                    className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-500/20"
                  >
                    Request 1-on-1 Session
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Active Study Groups Section */}
      <div className="space-y-4 pt-4 border-t border-slate-800">
        <h3 className="text-lg font-bold text-white">Active Peer Study Groups</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {groups.map((g) => (
            <div
              key={g.id}
              className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-indigo-400 font-semibold">{g.subject}</span>
                  {g.active_now && (
                    <span className="flex items-center space-x-1 text-emerald-400 font-bold text-[10px]">
                      <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span>Live Session</span>
                    </span>
                  )}
                </div>
                <h4 className="text-sm font-bold text-white">{g.title}</h4>
                <p className="text-xs text-slate-400 mt-2 line-clamp-3">{g.description}</p>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span>{g.member_count} members</span>
                <button
                  onClick={() => alert(`Joined ${g.title}!`)}
                  className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold"
                >
                  Join Circle
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Mentorship Booking Modal */}
      {selectedMentor && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
          <div className="relative w-full max-w-lg rounded-2xl bg-slate-900 border border-slate-700 p-6 shadow-2xl space-y-4">
            <button
              onClick={() => setSelectedMentor(null)}
              className="absolute right-4 top-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="flex items-center space-x-3">
              <img
                src={selectedMentor.avatar_url}
                alt={selectedMentor.name}
                className="h-12 w-12 rounded-xl object-cover border border-slate-700"
              />
              <div>
                <h4 className="text-base font-bold text-white">
                  Book Session with {selectedMentor.name}
                </h4>
                <p className="text-xs text-indigo-300">{selectedMentor.title}</p>
              </div>
            </div>

            {bookingSuccess ? (
              <div className="p-4 rounded-xl bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-sm text-center space-y-2">
                <CheckCircle className="h-8 w-8 text-emerald-400 mx-auto" />
                <p className="font-bold">{bookingSuccess}</p>
              </div>
            ) : (
              <form onSubmit={handleBook} className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Your Full Name</label>
                  <input
                    type="text"
                    required
                    value={learnerName}
                    onChange={(e) => setLearnerName(e.target.value)}
                    placeholder="e.g. Rahul Verma"
                    className="w-full p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Your Email</label>
                  <input
                    type="email"
                    required
                    value={learnerEmail}
                    onChange={(e) => setLearnerEmail(e.target.value)}
                    placeholder="e.g. rahul@example.com"
                    className="w-full p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Preferred Date</label>
                    <input
                      type="date"
                      value={prefDate}
                      onChange={(e) => setPrefDate(e.target.value)}
                      className="w-full p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-300 font-semibold mb-1">Preferred Time</label>
                    <input
                      type="text"
                      value={prefTime}
                      onChange={(e) => setPrefTime(e.target.value)}
                      placeholder="e.g. 6:00 PM IST"
                      className="w-full p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    What topic or questions would you like to discuss?
                  </label>
                  <textarea
                    rows={3}
                    required
                    value={topicDesc}
                    onChange={(e) => setTopicDesc(e.target.value)}
                    placeholder="e.g., I'd like help understanding semiconductor barrier potentials and diode applications..."
                    className="w-full p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500 resize-none"
                  />
                </div>

                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-sm shadow-lg shadow-indigo-500/25 transition-all"
                  >
                    {submitting ? 'Confirming...' : 'Confirm Mentorship Booking'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
