import React, { useState, useRef, useEffect } from 'react';
import {
  Bot, Send, Sparkles, BookOpen, CheckCircle, HelpCircle,
  Lightbulb, ArrowRight, RefreshCw, Code2, Compass
} from 'lucide-react';
import { api } from '../api/client';

export default function ChatTutor({ defaultTopic = 'Recursion' }) {
  const [topic, setTopic] = useState(defaultTopic);
  const [message, setMessage] = useState('');
  const [style, setStyle] = useState('step_by_step');
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'bot',
      text: `Hey there! I'm your Knowlix Socratic AI Tutor. 🎓\n\nI'm ready to help you explore and master **${defaultTopic}**. We can solve real practice problems together, debug tricky concepts, or break things down step-by-step.\n\nWhat would you like to work on right now?`,
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

  const styles = [
    { id: 'step_by_step', label: 'Step-by-Step' },
    { id: 'analogy', label: 'Everyday Analogy' },
    { id: 'practice', label: 'Practice Problem' },
    { id: 'simple', label: 'Simple & Plain' },
    { id: 'example_based', label: 'Example-First' },
  ];

  const quickStarters = [
    { label: 'Walk me through a problem', prompt: `Can we solve a step-by-step problem on ${topic}? Walk me through it without giving away the answer right away.` },
    { label: 'Explain with an analogy', prompt: `Can you explain the core mechanism of ${topic} using a relatable everyday analogy?` },
    { label: 'Give me a practice challenge', prompt: `Give me a diagnostic practice question or code drill on ${topic} to test my understanding.` },
    { label: 'Why is this so tricky?', prompt: `What is the most common mistake students make in ${topic}, and how do I avoid it?` },
  ];

  const handleSend = async (textToSend) => {
    const userMsg = (textToSend || message).trim();
    if (!userMsg || loading) return;

    setMessage('');
    const newChat = [...chatHistory, { sender: 'user', text: userMsg }];
    setChatHistory(newChat);
    setLoading(true);

    // Format previous history for Gemini
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
          text: `I ran into an issue connecting to the learning model: ${err.message}. Please try again!`,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSend();
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden flex flex-col h-[700px] shadow-sm">
      {/* Tutor Header & Controls */}
      <div className="p-4 border-b border-slate-100 bg-[#faf8fd] flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-[#342767] text-white flex items-center justify-center font-bold shadow-xs">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-sm">Knowlix Socratic Tutor</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Active Pair Learning
              </span>
            </div>
            <div className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
              <span>Topic:</span>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="font-bold text-slate-800 bg-white px-2 py-0.5 rounded-md border border-slate-300 text-xs w-36 focus:outline-none focus:ring-1 focus:ring-[#6e46e6]"
              />
            </div>
          </div>
        </div>

        {/* Teaching Style Pills */}
        <div className="flex items-center gap-1 bg-[#f2f2f7] p-1 rounded-xl text-xs">
          {styles.map((s) => (
            <button
              key={s.id}
              onClick={() => setStyle(s.id)}
              className={`px-3 py-1.5 rounded-lg transition font-medium text-xs ${
                style === s.id
                  ? 'bg-white text-slate-900 shadow-xs font-bold'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Problem Solving Starters */}
      <div className="px-6 py-2.5 bg-white border-b border-slate-100 flex items-center gap-2 overflow-x-auto text-xs">
        <span className="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1 whitespace-nowrap">
          <Lightbulb className="w-3.5 h-3.5 text-amber-500" /> Quick Starters:
        </span>
        {quickStarters.map((qs, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(qs.prompt)}
            disabled={loading}
            className="px-3 py-1 rounded-full border border-slate-200 hover:border-[#6e46e6] hover:bg-[#faf8fe] text-slate-600 hover:text-[#6e46e6] transition text-xs whitespace-nowrap font-medium"
          >
            {qs.label}
          </button>
        ))}
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-6 overflow-y-auto space-y-5 bg-[#fcfbfe]">
        {chatHistory.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed shadow-xs ${
                msg.sender === 'user'
                  ? 'bg-[#342767] text-white rounded-br-xs'
                  : 'bg-white text-slate-800 rounded-bl-xs border border-slate-100'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.text}</div>

              {/* Socratic Check-In Box */}
              {msg.checkQuestion && (
                <div className="mt-3.5 p-3.5 bg-[#fbf9fe] border border-dashed border-[#cbb8f7] rounded-xl text-slate-800 text-xs">
                  <div className="font-bold flex items-center gap-1.5 mb-1 text-[#6e46e6]">
                    <HelpCircle className="w-4 h-4 text-[#6e46e6]" />
                    Socratic Checkpoint:
                  </div>
                  <div className="text-slate-700 font-medium">{msg.checkQuestion}</div>
                  <button
                    onClick={() => {
                      setMessage(`Regarding that checkpoint: `);
                    }}
                    className="mt-2 text-[11px] font-bold text-[#6e46e6] hover:underline flex items-center gap-1"
                  >
                    <span>Reply to this check</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              )}

              {/* Verified Curriculum Sources */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-slate-100 text-[11px] text-slate-400 flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-slate-400" />
                  <span>Grounded in: <strong>{msg.citations.join(', ')}</strong></span>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 p-3 bg-white rounded-xl border border-slate-100 w-fit text-slate-500 text-xs shadow-xs">
            <Sparkles className="w-4 h-4 animate-spin text-[#6e46e6]" />
            <span>Knowlix is analyzing curriculum & scaffolding your response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <form onSubmit={handleFormSubmit} className="p-4 border-t border-slate-100 bg-white flex gap-2 items-center">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={`Ask a question, paste code, or type your answer for ${topic}...`}
          className="flex-1 px-4 py-3 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#4c35b5] focus:border-[#4c35b5] text-slate-800 placeholder-slate-400"
        />
        <button
          type="submit"
          disabled={loading || !message.trim()}
          className="px-6 py-3 bg-[#342767] hover:bg-[#281d52] disabled:opacity-40 text-white rounded-xl text-sm font-semibold flex items-center gap-2 shadow-xs transition duration-150"
        >
          <span>Send</span>
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
