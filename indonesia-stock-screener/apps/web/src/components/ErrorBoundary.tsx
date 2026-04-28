"use client";

import React, { Component, ReactNode } from 'react';
import { AlertCircle } from 'lucide-react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <section className="flex-1 bg-[#1d1b20] flex flex-col h-full overflow-hidden justify-center items-center">
          <div className="flex flex-col items-center gap-4 text-zinc-500">
            <AlertCircle className="w-12 h-12 text-rose-500/50" />
            <h2 className="font-['Inter'] font-semibold text-[18px] text-zinc-400">Data Feed Unavailable</h2>
            <p className="font-['Inter'] text-[13px] max-w-sm text-center">
              The valuation engine could not be reached. Please check your connection or try again later.
            </p>
            <button
                className="mt-4 border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 px-4 py-2 font-['Inter'] text-[13px] transition-colors rounded-none"
                onClick={() => this.setState({ hasError: false })}
            >
              Retry Connection
            </button>
          </div>
        </section>
      );
    }

    return this.props.children;
  }
}
