import React, { useState } from 'react';
import { Network, CheckCircle2, AlertTriangle, HelpCircle, ArrowRight } from 'lucide-react';

export default function KnowledgeGraphViewer({ graphData, onSelectTopic }) {
  const [selectedNode, setSelectedNode] = useState(null);

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-500">
        <Network className="w-10 h-10 mx-auto text-slate-300 mb-2" />
        <p>No knowledge graph data available for this subject.</p>
      </div>
    );
  }

  const { nodes, edges } = graphData;

  const getNodeColor = (status, score) => {
    if (score !== null && score !== undefined) {
      if (score >= 75) return 'bg-emerald-50 border-emerald-500 text-emerald-900';
      if (score >= 60) return 'bg-amber-50 border-amber-500 text-amber-900';
      return 'bg-rose-50 border-rose-500 text-rose-900';
    }
    return 'bg-slate-50 border-slate-300 text-slate-700';
  };

  const getBadge = (status, score) => {
    if (score !== null && score !== undefined) {
      if (score >= 75) return <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-100 text-emerald-700">Mastered ({score}%)</span>;
      if (score >= 60) return <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-100 text-amber-700">In Progress ({score}%)</span>;
      return <span className="text-xs font-semibold px-2 py-0.5 rounded bg-rose-100 text-rose-700">Struggling ({score}%)</span>;
    }
    return <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600">Unassessed</span>;
  };

  return (
    <div className="space-y-6">
      {/* Legend */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 text-xs">
        <div className="font-semibold text-slate-700">Mastery Status:</div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            <span>Mastered (≥75%)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-amber-500"></span>
            <span>In Progress (60-74%)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500"></span>
            <span>Struggling (&lt;60%)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-slate-400"></span>
            <span>Unassessed</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Node Grid */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200">
          <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">
            Curriculum Concepts & Prerequisite Flow
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {nodes.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              return (
                <div
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    getNodeColor(node.status, node.score)
                  } ${isSelected ? 'ring-2 ring-brand-500 shadow-sm' : 'hover:border-slate-400'}`}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="text-xs uppercase font-semibold text-slate-500">{node.chapter}</span>
                    {getBadge(node.status, node.score)}
                  </div>
                  <h4 className="font-bold text-sm text-slate-900">{node.label}</h4>
                  <div className="mt-2 text-xs text-slate-500 flex items-center justify-between">
                    <span>Difficulty: <strong className="capitalize text-slate-700">{node.difficulty}</strong></span>
                    {isSelected && <span className="text-brand-600 font-semibold flex items-center gap-1">Selected <ArrowRight className="w-3 h-3" /></span>}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Concept Detail Pane */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">
              Concept Deep-Dive
            </h3>
            {selectedNode ? (
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-slate-400 uppercase tracking-wider">{selectedNode.subject} • {selectedNode.chapter}</div>
                  <h4 className="text-xl font-bold text-slate-900 mt-1">{selectedNode.label}</h4>
                </div>

                <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Mastery Score:</span>
                    <span className="font-bold text-slate-800">{selectedNode.score !== null ? `${selectedNode.score}%` : 'Not assessed'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Curriculum Tier:</span>
                    <span className="font-bold capitalize text-slate-800">{selectedNode.difficulty}</span>
                  </div>
                </div>

                <div>
                  <h5 className="text-xs font-bold text-slate-700 uppercase mb-2">Prerequisites:</h5>
                  {edges.filter(e => e.target === selectedNode.id).length > 0 ? (
                    <div className="space-y-1.5">
                      {edges.filter(e => e.target === selectedNode.id).map(e => {
                        const prereqNode = nodes.find(n => n.id === e.source);
                        return (
                          <div key={e.source} className="text-xs p-2 bg-slate-100 rounded flex items-center justify-between">
                            <span className="font-medium text-slate-800">{prereqNode ? prereqNode.label : `Topic #${e.source}`}</span>
                            <span className="text-[10px] text-brand-700 bg-brand-50 px-1.5 py-0.5 rounded font-semibold uppercase">{e.strength}</span>
                          </div>
                        );
                      })}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">No prerequisite requirements. Foundational entry concept.</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-400 text-sm">
                <HelpCircle className="w-8 h-8 mx-auto text-slate-300 mb-2" />
                Select any concept node to inspect its prerequisites and mastery signals.
              </div>
            )}
          </div>

          {selectedNode && onSelectTopic && (
            <button
              onClick={() => onSelectTopic(selectedNode.label)}
              className="mt-6 w-full py-2.5 px-4 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition"
            >
              <span>Practice / Ask AI Tutor</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

