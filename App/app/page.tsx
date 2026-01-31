'use client';

import React, { useState } from 'react';
import { 
  Plus, Search, Globe, ChevronDown, Upload, 
  Sparkles, MessageSquare, Mic, Video, Network, 
  FileText, Layers, PieChart, Send, MoreVertical,
  PanelLeftClose, PanelRightClose
} from 'lucide-react';

export default function Dashboard() {
  const [query, setQuery] = useState('');

  return (
    <div className="flex h-screen bg-[#1e1e1e] text-gray-200 font-sans overflow-hidden">
      
      {/* ================= LEFT SIDEBAR: SOURCES ================= */}
      <aside className="w-[300px] flex flex-col border-r border-gray-800 bg-[#1e1e1e] p-4 flex-shrink-0">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-medium text-gray-100">Sources</h2>
          <PanelLeftClose className="w-5 h-5 text-gray-400 cursor-pointer hover:text-white" />
        </div>

        {/* Add Sources Button */}
        <button className="flex items-center justify-center gap-2 w-full py-2.5 rounded-full border border-gray-600 hover:bg-gray-800 transition-colors text-sm font-medium mb-4">
          <Plus className="w-4 h-4" />
          Add sources
        </button>

        {/* Search Bar */}
        <div className="bg-[#2a2a2a] rounded-2xl border border-gray-700 p-3 mb-auto">
          <div className="flex items-center gap-2 text-gray-400 mb-2">
            <Search className="w-4 h-4" />
            <span className="text-sm">Search the web for new sources</span>
          </div>
          <div className="flex gap-2 mt-2">
            <button className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#333] text-xs hover:bg-[#444] border border-gray-600">
              <Globe className="w-3 h-3" />
              Web
              <ChevronDown className="w-3 h-3" />
            </button>
            <button className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#333] text-xs hover:bg-[#444] border border-gray-600">
              <Sparkles className="w-3 h-3" />
              Fast research
              <ChevronDown className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* Empty State for Sources */}
        <div className="mt-8 flex flex-col items-center text-center opacity-60">
          <FileText className="w-8 h-8 mb-2 text-gray-500" />
          <p className="text-xs text-gray-400">Saved sources will appear here</p>
        </div>
      </aside>


      {/* ================= CENTER PANEL: CHAT ================= */}
      <main className="flex-1 flex flex-col relative bg-[#1e1e1e]">
        {/* Header / Top Bar */}
        <header className="flex justify-between items-center p-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
             {/* Removed Logo, Just Text */}
             <span className="font-medium text-lg text-gray-100">Notebook</span>
          </div>
          <div className="flex items-center gap-3">
             {/* Renamed Button, Removed Profile/Settings */}
             <button className="text-xs font-medium px-3 py-1.5 rounded-full bg-white text-black hover:bg-gray-200 flex items-center gap-1">
               <Plus className="w-3 h-3" /> New Notebook
             </button>
          </div>
        </header>

        {/* Empty State Content */}
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <div className="w-16 h-16 rounded-full bg-[#2a2a2a] flex items-center justify-center mb-6">
            <Upload className="w-8 h-8 text-blue-400" />
          </div>
          <h1 className="text-2xl font-light mb-2">Add a source to get started</h1>
          <button className="mt-4 px-6 py-2.5 bg-[#2a2a2a] border border-gray-600 rounded-full text-sm font-medium hover:bg-[#333] transition-colors">
            Upload a source
          </button>
        </div>

        {/* Chat Input Area */}
        <div className="p-4 w-full max-w-3xl mx-auto mb-4">
          <div className="bg-[#2a2a2a] border border-gray-700 rounded-3xl p-4 flex items-center gap-3 shadow-lg">
             <input 
                type="text" 
                placeholder="Upload a source to get started" 
                className="flex-1 bg-transparent outline-none text-sm placeholder-gray-500"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled
             />
             <div className="flex items-center gap-2 text-gray-500">
                <span className="text-xs">0 sources</span>
                <button className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center opacity-50 cursor-not-allowed">
                  <Send className="w-4 h-4 text-white" />
                </button>
             </div>
          </div>
          <p className="text-center text-[10px] text-gray-500 mt-2">
            NotebookLM can be inaccurate; please double-check its responses.
          </p>
        </div>
      </main>


      {/* ================= RIGHT SIDEBAR: STUDIO ================= */}
      <aside className="w-[320px] flex flex-col border-l border-gray-800 bg-[#1e1e1e] p-5 flex-shrink-0">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-medium text-gray-100">Studio</h2>
          <PanelRightClose className="w-5 h-5 text-gray-400 cursor-pointer hover:text-white" />
        </div>

        {/* Studio Grid */}
        <div className="grid grid-cols-2 gap-3">
            <StudioCard icon={<Mic />} label="Audio Overview" />
            <StudioCard icon={<Video />} label="Video Overview" />
            <StudioCard icon={<Network />} label="Mind Map" />
            <StudioCard icon={<FileText />} label="Reports" />
            <StudioCard icon={<Layers />} label="Flashcards" />
            <StudioCard icon={<MessageSquare />} label="Quiz" />
            <StudioCard icon={<PieChart />} label="Infographic" />
            <StudioCard icon={<MoreVertical />} label="Slide deck" />
        </div>

        {/* Bottom Helper */}
        <div className="mt-auto pt-10 flex flex-col items-center text-center opacity-70">
           <Sparkles className="w-5 h-5 text-gray-400 mb-2" />
           <p className="text-xs text-gray-400 max-w-[200px]">
             Studio output will be saved here. After adding sources, click to add Audio Overview, study guide, mind map and more!
           </p>
        </div>

        {/* Add Note Button */}
        <button className="mt-8 w-full py-2.5 bg-white text-black rounded-full font-medium text-sm flex items-center justify-center gap-2 hover:bg-gray-200">
          <FileText className="w-4 h-4" /> Add note
        </button>
      </aside>

    </div>
  );
}

// Helper Component for the Studio Grid Cards
function StudioCard({ icon, label }: { icon: any, label: string }) {
  return (
    <div className="bg-[#262626] hover:bg-[#333] transition-colors p-4 rounded-xl flex flex-col items-start gap-3 cursor-pointer group border border-transparent hover:border-gray-700">
      <div className="text-gray-400 group-hover:text-blue-400 transition-colors">
        {React.cloneElement(icon, { size: 20 })}
      </div>
      <span className="text-xs font-medium text-gray-300 group-hover:text-white">{label}</span>
    </div>
  );
}