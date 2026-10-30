import React, { useState, useRef, useEffect } from 'react';
import {
  Bot, Send, Sparkles, BookOpen, HelpCircle,
  Lightbulb, ArrowRight, RefreshCw, Code, CheckCircle,
  Cpu, Wrench, FileQuestion, BookMarked
} from 'lucide-react';
import { api } from '../api/client';

export default function ChatTutor({ defaultTopic = 'Recursion' }) {
  const [topic, setTopic] = useState(defaultTopic);
  const [isCustomTopic, setIsCustomTopic] = useState(false);
  const [message, setMessage] = useState('');
  const [style, setStyle] = useState('step_by_step');
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'bot',
      text: `Hello! I'm your Knowlix AI Tutor. 🎓\n\nI can help you solve **any problem or homework question** you have. You can:\n• Paste a math equation, physics problem, or code snippet\n• Ask me to walk you through a problem step-by-step\n• Paste your attempt and ask me to find your mistake\n• Ask for an intuitive everyday analogy\n\nWhat problem would you like to work on right now?`,
      style: 'step_by_step',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, loading]);

  const presetTopics = [
    'Recursion',
    'Quadratic Equations',
    'Photosynthesis',
    'Arrays & Lists',
    'Calculus & Derivatives',
    'Physics & Mechanics',
  ];

  const modes = [
    { id: 'step_by_step', label: 'Step-by-Step Solver', icon: Wrench, desc: 'Guided walkthrough of your problem' },
    { id: 'analogy', label: 'Everyday Analogy', icon: Lightbulb, desc: 'Intuitive real-world metaphors' },
    { id: 'practice', label: 'Practice Drills', icon: FileQuestion, desc: 'Diagnostic micro-quizzes' },
    { id: 'example_based', label: 'Worked Examples', icon: Code, desc: 'Concrete code & formula demos' },
  ];

  const followUpSuggestions = [
    'Give me a hint on what to do next',
    'Can you show me a similar small example?',
    'Why is this step necessary?',
    'Please show me the full complete solution',
  ];

  const handleSend = async (textToSend) => {
    const userMsg = (textToSend || message).trim();
    if (!userMsg || loading) return;

    setMessage('');
    const newChat = [...chatHistory, { sender: 'user', text: userMsg }];
    setChatHistory(newChat);
    setLoading(true);

    // Multi-turn context payload
    const historyPayload = newChat.slice(0, -1).map((m) => ({
      role: m.sender === 'user' ? 'user' : 'assistant',
      content: m.text,
    }));

    try {
      const res = await api.tutorChat(topic, userMsg, style, historyPayload);
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
          text: `I ran into an issue connecting to Gemini: ${err.message}. Please try again!`,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleResetChat = () => {
    setChatHistory([
      {
        sender: 'bot',
        text: `Starting a fresh problem session for **${topic}**! What question or problem do you want to solve?`,
        style: style,
      },
    ]);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[720px]">
      {/* Top Controls Bar */}
      <div className="p-4 bg-slate-50 border-b border-slate-200 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold shadow-xs">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-900 text-sm">Knowlix Interactive AI Tutor</span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  Gemini Live
                </span>
              </div>
              <div className="text-xs text-slate-500 flex items-center gap-2 mt-0.5">
                <span>Active Topic:</span>
                {isCustomTopic ? (
                  <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="Type any subject/topic..."
                    className="font-semibold text-slate-900 bg-white px-2 py-0.5 rounded border border-brand-400 text-xs w-48 focus:outline-none"
                    autoFocus
                  />
                ) : (
                  <select
                    value={topic}
                    onChange={(e) => {
                      if (e.target.value === 'custom') {
                        setIsCustomTopic(true);
                        setTopic('');
                      } else {
                        setTopic(e.target.value);
                      }
                    }}
                    className="font-semibold text-slate-800 bg-white px-2 py-0.5 rounded border border-slate-300 text-xs"
                  >
                    {presetTopics.map((pt) => (
                      <option key={pt} value={pt}>{pt}</option>
                    ))}
                    <option value="custom">✏️ Type your own custom topic...</option>
                  </select>
                )}
                {isCustomTopic && (
                  <button
                    onClick={() => {
                      setIsCustomTopic(false);
                      setTopic('Recursion');
                    }}
                    className="text-[11px] text-brand-600 hover:underline font-semibold"
                  >
                    Reset
                  </button>
                )}
              </div>
            </div>
          </div>

          <button
            onClick={handleResetChat}
            className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-800 px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 transition"
            title="Start a new question"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>New Problem</span>
          </button>
        </div>

        {/* Tutoring Mode Selector */}
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <span className="text-[11px] font-bold uppercase text-slate-400 mr-1">Mode:</span>
          {modes.map((m) => {
            const Icon = m.icon;
            const isSelected = style === m.id;
            return (
              <button
                key={m.id}
                onClick={() => setStyle(m.id)}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition ${
                  isSelected
                    ? 'bg-brand-600 text-white shadow-xs'
                    : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
                title={m.desc}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{m.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-50/50">
        {chatHistory.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-brand-600 text-white rounded-br-xs shadow-xs'
                  : 'bg-white text-slate-800 rounded-bl-xs border border-slate-200 shadow-xs'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.text}</div>

              {/* Socratic Checkpoint Card */}
              {msg.checkQuestion && (
                <div className="mt-3 p-3 bg-amber-50/70 border border-amber-200 rounded-xl text-slate-800 text-xs">
                  <div className="font-bold flex items-center gap-1.5 mb-1 text-amber-800">
                    <CheckCircle className="w-3.5 h-3.5 text-amber-600" />
                    Socratic Question for You:
                  </div>
                  <div className="text-slate-700 font-medium">{msg.checkQuestion}</div>
                  <button
                    onClick={() => {
                      setMessage(`Regarding that: `);
                    }}
                    className="mt-2 text-[11px] font-bold text-brand-600 hover:underline flex items-center gap-1"
                  >
                    <span>Click to reply to this question</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              )}

              {/* Curriculum Source Citation */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-400 flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-slate-400" />
                  <span>Curriculum Source: {msg.citations.join(', ')}</span>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 p-3 bg-white rounded-xl border border-slate-200 w-fit text-slate-500 text-xs shadow-xs">
            <Sparkles className="w-4 h-4 animate-spin text-brand-600" />
            <span>Knowlix is solving & reasoning step-by-step with Gemini...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Follow-Ups Pills */}
      <div className="px-4 py-2 bg-slate-50 border-t border-slate-200 flex items-center gap-2 overflow-x-auto text-xs">
        <span className="text-slate-400 font-bold uppercase text-[10px] whitespace-nowrap">Suggested:</span>
        {followUpSuggestions.map((sug, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(sug)}
            disabled={loading}
            className="px-2.5 py-1 bg-white hover:bg-slate-100 border border-slate-200 rounded-full text-slate-600 hover:text-slate-900 text-xs whitespace-nowrap transition"
          >
            {sug}
          </button>
        ))}
      </div>

      {/* User Input Form */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="p-4 border-t border-slate-200 bg-white flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={`Ask ANY question or problem in ${topic || 'any subject'}...`}
          className="flex-1 px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-800"
        />
        <button
          type="submit"
          disabled={loading || !message.trim()}
          className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-40 text-white rounded-xl text-sm font-semibold flex items-center gap-2 transition"
        >
          <span>Send</span>
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
