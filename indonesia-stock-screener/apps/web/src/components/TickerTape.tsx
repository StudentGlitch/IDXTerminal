import React from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';

export function TickerTape() {
  return (
    <div className="bg-zinc-950 border-b border-zinc-800 h-8 flex items-center px-3 gap-6 overflow-hidden whitespace-nowrap text-[11px] font-['JetBrains_Mono'] shrink-0">
      <div className="flex items-center gap-2">
        <span className="text-zinc-400 font-medium">IHSG</span>
        <span className="text-zinc-100 font-medium">7,200.50</span>
        <span className="text-emerald-500 flex items-center"><ChevronUp className="w-3 h-3" />0.4%</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-zinc-400 font-medium">USD/IDR</span>
        <span className="text-zinc-100 font-medium">15,750</span>
        <span className="text-rose-500 flex items-center"><ChevronDown className="w-3 h-3" />0.1%</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-zinc-400 font-medium">LQ45</span>
        <span className="text-zinc-100 font-medium">980.25</span>
        <span className="text-emerald-500 flex items-center"><ChevronUp className="w-3 h-3" />0.2%</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-zinc-400 font-medium">IDX30</span>
        <span className="text-zinc-100 font-medium">512.10</span>
        <span className="text-rose-500 flex items-center"><ChevronDown className="w-3 h-3" />0.05%</span>
      </div>
    </div>
  );
}
