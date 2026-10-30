import React, { useState } from 'react';
import { Bot, Send, Sparkles, BookOpen, Layers, CheckCircle } from 'lucide-react';
import { api } from '../api/client';

export default function ChatTutor({ defaultTopic = 'Recursion' }) {
  const [topic, setTopic] = useState(defaultTopic);
  const [message, setMessage] = useState('');
  const [style, setStyle] = useState('step_by_step');
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'bot',
      text: `Hello! I'm your Knowlix AI Tutor. I'm currently set to explain concepts in **${topic}**. You can choose your preferred teaching style below or ask any question!`,
      style: 'step_by_step',
    },
  ]);
  const [loading, setLoading] = useState(false);

  const styles = [
    { id: 'step_by_step', label: 'Step-by-Step' },
    { id: 'analogy', label: 'Everyday Analogy' },
    { id: 'simple', label: 'Simple & Intuitive' },
    { id: 'example_based', label: 'Example-First' },
    { id: 'practice', label: 'Practice Drill' },
  ];

  const handleSend = async (e) => {
    e.preventDefault();
    if (!message.trim() || loading) return;

    const userMsg = message.trim();
    setMessage('');
    setChatHistory((prev) => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const res = await api.tutorChat(topic, userMsg, style);
      setChatHistory((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: res.reply,
          checkQuestion: res.comprehension_check,
          citations: res.citations,
          style: res.pedagogical_style,
        },
      ]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: `I encountered an issue retrieving curriculum data: ${err.message}. Please try again.`,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden flex flex-col h-[650px]">
      {/* Tutor Header & Controls */}
      <div className="p-4 border-b border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-brand-600 text-white flex items-center justify-center font-bold">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="font-bold text-slate-900 text-sm">Knowlix Adaptive AI Tutor</div>
            <div className="text-xs text-slate-500 flex items-center gap-1.5">
              <span>Topic:</span>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="font-semibold text-slate-800 bg-white px-2 py-0.5 rounded border border-slate-300 text-xs w-36"
              />
            </div>
          </div>
        </div>

        {/* Style Selector */}
        <div className="flex items-center gap-1 bg-white p-1 rounded-lg border border-slate-200 text-xs">
          {styles.map((s) => (
            <button
              key={s.id}
              onClick={() => setStyle(s.id)}
              className={`px-2.5 py-1 rounded-md transition font-medium ${
                style === s.id
                  ? 'bg-brand-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4">
        {chatHistory.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-brand-600 text-white rounded-br-xs'
                  : 'bg-slate-100 text-slate-800 rounded-bl-xs border border-slate-200'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.text}</div>

              {/* Comprehension Check Box */}
              {msg.checkQuestion && (
                <div className="mt-3 p-3 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-xs">
                  <div className="font-bold flex items-center gap-1.5 mb-1 text-amber-800">
                    <CheckCircle className="w-3.5 h-3.5 text-amber-600" />
                    Quick Check for Understanding:
                  </div>
                  <div>{msg.checkQuestion}</div>
                </div>
              )}

              {/* Curriculum Citations */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 text-[11px] text-slate-500 flex items-center gap-1">
                  <BookOpen className="w-3 h-3 text-slate-400" />
                  <span>Curriculum Sources: {msg.citations.join(', ')}</span>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-slate-400 text-xs italic">
            <Sparkles className="w-4 h-4 animate-spin text-brand-600" />
            <span>Analyzing student learning state & retrieving curriculum...</span>
          </div>
        )}
      </div>

      {/* Input Bar */}
      <form onSubmit={handleSend} className="p-4 border-t border-slate-200 bg-white flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={`Ask about ${topic} or reply to the check question...`}
          className="flex-1 px-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
        />
        <button
          type="submit"
          disabled={loading || !message.trim()}
          className="px-5 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white rounded-lg text-sm font-semibold flex items-center gap-2 transition"
        >
          <span>Send</span>
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}

