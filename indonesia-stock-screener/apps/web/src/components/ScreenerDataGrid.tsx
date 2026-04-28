"use client";

import React, { useState } from 'react';
import useSWR from 'swr';
import { Download, Columns } from 'lucide-react';
import { Button } from '@/components/ui/button';

// Helper for fetching data
const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface StockScreenerData {
  ticker: string;
  company_name: string;
  current_price: number;
  dcf_value: number | null;
  margin_of_safety: number | null;
  forward_pe: number | null;
  piotroski_f_score: number | null;
}

interface ApiResponse {
    data: StockScreenerData[];
}

export function ScreenerDataGrid() {
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 20;

  const { data: response, error, isLoading } = useSWR<ApiResponse>(
    'http://127.0.0.1:8000/api/screener/',
    fetcher,
    {
        onError: (err) => {
            console.error("SWR Error fetching data:", err);
            // Optionally throw error to be caught by the ErrorBoundary,
            // but Next.js/React error boundaries don't catch async errors like this naturally.
            // We'll throw it during render if `error` is populated.
        }
    }
  );

  if (error) {
      throw error; // Let the ErrorBoundary catch it
  }

  const data = response?.data;

  // Pagination logic
  const totalItems = data ? data.length : 0;
  const totalPages = Math.ceil(totalItems / rowsPerPage);

  const startIndex = (currentPage - 1) * rowsPerPage;
  const paginatedData = data ? data.slice(startIndex, startIndex + rowsPerPage) : [];

  return (
    <section className="flex-1 bg-[#1d1b20] flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-3 border-b border-zinc-800 flex justify-between items-center bg-zinc-900 shrink-0">
        <div className="flex items-center gap-4">
          <h1 className="font-['Inter'] font-semibold text-[18px] text-[#e6e0e9]">Screen Results</h1>
          <span className="bg-zinc-800 text-zinc-300 font-['Inter'] text-[11px] px-2 py-0.5 rounded-none border border-zinc-700">
            {data ? `${data.length} Matches` : 'Loading...'}
          </span>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="border-zinc-700 bg-zinc-900 hover:bg-zinc-800 hover:text-zinc-300 text-zinc-300 px-3 py-1 flex items-center gap-1 font-['Inter'] text-[11px] transition-colors rounded-none h-auto">
            <Download className="w-3.5 h-3.5" /> Export
          </Button>
          <Button variant="outline" className="border-zinc-700 bg-zinc-900 hover:bg-zinc-800 hover:text-zinc-300 text-zinc-300 px-3 py-1 flex items-center gap-1 font-['Inter'] text-[11px] transition-colors rounded-none h-auto">
            <Columns className="w-3.5 h-3.5" /> Columns
          </Button>
        </div>
      </div>

      {/* DataTable Container */}
      <div className="flex-1 overflow-auto bg-zinc-950">
        <table className="w-full text-left border-collapse">
          <thead className="sticky top-0 bg-zinc-900 z-10 shadow-[0_1px_0_0_#27272a]">
            <tr>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 w-24">Ticker</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800">Name</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 text-right">Price (IDR)</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 text-right">MoS</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 text-right">DCF Value</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 text-right">Fwd P/E</th>
              <th className="px-2 py-1 font-['Inter'] text-[11px] text-zinc-400 font-bold uppercase tracking-wider border-b border-zinc-800 text-center w-24">F-Score</th>
            </tr>
          </thead>
          <tbody className="font-['Inter'] text-[13px] text-zinc-200 font-medium">
            {isLoading && (
              <tr>
                <td colSpan={7} className="text-center py-4 text-zinc-500 font-['Inter'] text-[13px]">Loading data...</td>
              </tr>
            )}
            {error && (
              <tr>
                <td colSpan={7} className="text-center py-4 text-rose-500 font-['Inter'] text-[13px]">Failed to load data.</td>
              </tr>
            )}
            {paginatedData && paginatedData.map((stock, index) => {
              const mosValue = stock.margin_of_safety;
              const mosColor = mosValue !== null && mosValue > 0 ? "text-emerald-500" : mosValue !== null && mosValue < 0 ? "text-rose-500" : "text-zinc-400";
              const fScore = stock.piotroski_f_score;
              const fScoreBg = fScore !== null && fScore >= 7 ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : fScore !== null && fScore <= 3 ? "bg-rose-500/10 text-rose-500 border-rose-500/20" : "bg-zinc-500/10 text-zinc-400 border-zinc-500/20";

              return (
                <tr key={stock.ticker} className={`border-b border-zinc-800 hover:bg-zinc-900 transition-colors group cursor-pointer ${index === 1 ? "border-l-2 border-l-blue-500 bg-zinc-900/50" : ""}`}>
                  <td className="px-2 py-1 font-['JetBrains_Mono'] text-[13px] font-medium text-blue-400 tracking-[-0.02em]">{stock.ticker}</td>
                  <td className="px-2 py-1 truncate max-w-[200px]">{stock.company_name || 'Unknown Company'}</td>
                  <td className="px-2 py-1 font-['JetBrains_Mono'] text-[13px] font-medium text-right tracking-[-0.02em]">
                    {stock.current_price !== null ? stock.current_price.toLocaleString() : '-'}
                  </td>
                  <td className={`px-2 py-1 font-['JetBrains_Mono'] text-[13px] font-medium text-right tracking-[-0.02em] ${mosColor}`}>
                    {mosValue !== null ? `${(mosValue).toFixed(1)}%` : '-'}
                  </td>
                  <td className="px-2 py-1 font-['JetBrains_Mono'] text-[13px] font-medium text-right tracking-[-0.02em]">
                    {stock.dcf_value !== null ? Math.round(stock.dcf_value).toLocaleString() : '-'}
                  </td>
                  <td className="px-2 py-1 font-['JetBrains_Mono'] text-[13px] font-medium text-right tracking-[-0.02em]">
                    {stock.forward_pe !== null ? stock.forward_pe.toFixed(1) : '-'}
                  </td>
                  <td className="px-2 py-1 text-center">
                    {fScore !== null ? (
                      <span className={`inline-block px-1.5 py-0.5 border font-['JetBrains_Mono'] text-[11px] ${fScoreBg}`}>
                        {fScore}
                      </span>
                    ) : '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination / Status Bar */}
      <div className="h-8 border-t border-zinc-800 bg-zinc-950 flex justify-between items-center px-3 font-['JetBrains_Mono'] text-[11px] text-zinc-500 shrink-0">
        <div>
            Showing {totalItems > 0 ? `${startIndex + 1}-${Math.min(startIndex + rowsPerPage, totalItems)}` : '0-0'} of {totalItems} entries
        </div>
        <div className="flex gap-4 items-center">
          <button
            className="hover:text-zinc-300 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="text-zinc-200 bg-zinc-800 px-2 py-0.5 border border-zinc-700">{currentPage}</span>
          <button
            className="hover:text-zinc-300 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages || totalPages === 0}
          >
            Next
          </button>
        </div>
      </div>
    </section>
  );
}
