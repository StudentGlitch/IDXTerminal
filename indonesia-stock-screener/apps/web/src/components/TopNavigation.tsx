import React from 'react';
import { Search, Bell, Settings, Terminal } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function TopNavigation() {
  return (
    <header className="bg-zinc-950 flex justify-between items-center w-full px-3 gap-6 docked full-width top-0 h-12 border-b border-zinc-800 flat no-shadows level-0 shrink-0">
      <div className="flex items-center gap-6 h-full">
        <div className="font-bold text-zinc-50 tracking-tighter text-lg uppercase flex items-center gap-2">
          <Terminal className="w-5 h-5 fill-current" />
          IDX TERMINAL
        </div>
        <div className="flex items-center bg-zinc-900 border border-zinc-800 px-2 py-1 gap-2 focus-within:border-blue-500">
          <Search className="text-zinc-500 w-4 h-4" />
          <input
            className="bg-transparent border-none outline-none text-zinc-200 font-['Inter'] text-[13px] tracking-tight antialiased placeholder-zinc-600 p-0 focus:ring-0 w-48"
            placeholder="Search tickers, sectors..."
            type="text"
          />
        </div>
        <nav className="flex h-full items-center gap-6">
          <a className="text-blue-500 font-semibold border-b-2 border-blue-500 h-full flex items-center font-['Inter'] text-[13px] tracking-tight antialiased hover:bg-zinc-900 transition-colors duration-150 cursor-pointer active:opacity-80 px-2" href="#">Screener</a>
          <a className="text-zinc-400 font-medium hover:text-zinc-200 font-['Inter'] text-[13px] tracking-tight antialiased hover:bg-zinc-900 transition-colors duration-150 cursor-pointer active:opacity-80 px-2 h-full flex items-center border-b-2 border-transparent" href="#">Watchlist</a>
          <a className="text-zinc-400 font-medium hover:text-zinc-200 font-['Inter'] text-[13px] tracking-tight antialiased hover:bg-zinc-900 transition-colors duration-150 cursor-pointer active:opacity-80 px-2 h-full flex items-center border-b-2 border-transparent" href="#">Sectors</a>
          <a className="text-zinc-400 font-medium hover:text-zinc-200 font-['Inter'] text-[13px] tracking-tight antialiased hover:bg-zinc-900 transition-colors duration-150 cursor-pointer active:opacity-80 px-2 h-full flex items-center border-b-2 border-transparent" href="#">Analytics</a>
        </nav>
      </div>
      <div className="flex items-center gap-4">
        <button className="text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900 p-1 transition-colors duration-150 cursor-pointer active:opacity-80">
          <Bell className="w-5 h-5" />
        </button>
        <button className="text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900 p-1 transition-colors duration-150 cursor-pointer active:opacity-80">
          <Settings className="w-5 h-5" />
        </button>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white font-['Inter'] text-[13px] font-semibold px-3 py-1.5 transition-colors duration-150 rounded-none h-auto">
          Execute Trade
        </Button>
      </div>
    </header>
  );
}
