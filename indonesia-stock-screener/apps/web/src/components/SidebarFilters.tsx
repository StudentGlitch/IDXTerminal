"use client";

import React from 'react';
import { ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function SidebarFilters() {
  return (
    <aside className="w-64 bg-[#0f0d13] border-r border-zinc-800 flex flex-col h-full overflow-y-auto shrink-0">
      <div className="p-3 border-b border-zinc-800 bg-[#211f24] flex justify-between items-center">
        <h2 className="font-['Inter'] font-semibold text-[18px] text-[#e6e0e9]">Filters</h2>
        <button className="text-blue-500 hover:text-blue-400 font-['Inter'] text-[11px]">Reset</button>
      </div>
      <div className="p-4 flex flex-col gap-6">
        {/* Sector Dropdown */}
        <div className="flex flex-col gap-2">
          <label className="font-['Inter'] text-[11px] text-zinc-400 uppercase tracking-wider">Sector</label>
          <div className="relative">
            <select className="w-full bg-zinc-950 border border-zinc-800 text-zinc-200 font-['Inter'] text-[13px] py-1.5 pl-2 pr-8 appearance-none focus:border-blue-500 focus:ring-0 outline-none rounded-none cursor-pointer">
              <option value="all">All Sectors</option>
              <option value="idxic">IDXIC - Financials</option>
              <option value="idxen">IDXEN - Energy</option>
              <option value="idxbm">IDXBM - Basic Materials</option>
              <option value="idxnoncyc">IDXNONCYC - Consumer Non-Cyclicals</option>
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 text-zinc-500 w-4 h-4 pointer-events-none" />
          </div>
        </div>

        {/* P/E Ratio Slider Mock */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <label className="font-['Inter'] text-[11px] text-zinc-400 uppercase tracking-wider">P/E Ratio</label>
            <span className="font-['JetBrains_Mono'] text-[11px] text-zinc-300">0 - 50</span>
          </div>
          <div className="relative w-full h-1 bg-zinc-800 mt-2">
            <div className="absolute left-0 top-0 h-full bg-blue-500 w-full"></div>
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-zinc-200 border border-zinc-800 cursor-pointer"></div>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-zinc-200 border border-zinc-800 cursor-pointer"></div>
          </div>
        </div>

        {/* PBV Slider Mock */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <label className="font-['Inter'] text-[11px] text-zinc-400 uppercase tracking-wider">PBV</label>
            <span className="font-['JetBrains_Mono'] text-[11px] text-zinc-300">0 - 10</span>
          </div>
          <div className="relative w-full h-1 bg-zinc-800 mt-2">
            <div className="absolute left-0 top-0 h-full bg-blue-500 w-3/4"></div>
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-zinc-200 border border-zinc-800 cursor-pointer"></div>
            <div className="absolute left-3/4 top-1/2 -translate-y-1/2 w-3 h-3 bg-zinc-200 border border-zinc-800 cursor-pointer -translate-x-full"></div>
          </div>
        </div>

        {/* MoS Toggle */}
        <div className="flex items-center justify-between">
          <label className="font-['Inter'] text-[13px] font-medium text-zinc-300 cursor-pointer select-none">Margin of Safety &gt; 20%</label>
          <div className="relative inline-block w-8 mr-2 align-middle select-none transition duration-200 ease-in">
            <input defaultChecked className="toggle-checkbox absolute block w-4 h-4 rounded-none bg-zinc-200 border-2 border-zinc-800 appearance-none cursor-pointer checked:right-0 checked:bg-blue-500 checked:border-blue-500 z-10" id="mos-toggle" name="toggle" type="checkbox" />
            <label className="toggle-label block overflow-hidden h-4 rounded-none bg-zinc-800 cursor-pointer" htmlFor="mos-toggle"></label>
          </div>
        </div>

        {/* Piotroski Score Toggles */}
        <div className="flex flex-col gap-3 pt-4 border-t border-zinc-800">
          <label className="font-['Inter'] text-[11px] text-zinc-400 uppercase tracking-wider">Quality (F-Score)</label>
          <div className="flex flex-col gap-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input defaultChecked className="w-3 h-3 bg-zinc-950 border-zinc-700 text-blue-500 focus:ring-0 rounded-none cursor-pointer" type="checkbox" />
              <span className="font-['Inter'] text-[13px] text-zinc-300">Strong (7-9)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input defaultChecked className="w-3 h-3 bg-zinc-950 border-zinc-700 text-blue-500 focus:ring-0 rounded-none cursor-pointer" type="checkbox" />
              <span className="font-['Inter'] text-[13px] text-zinc-300">Typical (4-6)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input className="w-3 h-3 bg-zinc-950 border-zinc-700 text-blue-500 focus:ring-0 rounded-none cursor-pointer" type="checkbox" />
              <span className="font-['Inter'] text-[13px] text-zinc-500">Weak (0-3)</span>
            </label>
          </div>
        </div>
      </div>

      <div className="mt-auto p-4 border-t border-zinc-800">
        <Button className="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-100 font-['Inter'] text-[13px] py-2 border border-zinc-700 transition-colors rounded-none h-auto">
          Apply Filters
        </Button>
      </div>
    </aside>
  );
}
