import { TopNavigation } from '@/components/TopNavigation';
import { TickerTape } from '@/components/TickerTape';
import { SidebarFilters } from '@/components/SidebarFilters';
import { ScreenerDataGrid } from '@/components/ScreenerDataGrid';
import { ErrorBoundary } from '@/components/ErrorBoundary';

export default function Home() {
  return (
    <div className="bg-background text-on-surface h-screen flex flex-col font-ui-medium text-ui-medium overflow-hidden selection:bg-primary selection:text-on-primary">
      <TopNavigation />
      <TickerTape />

      <main className="flex-1 flex overflow-hidden">
        <SidebarFilters />
        <ErrorBoundary>
          <ScreenerDataGrid />
        </ErrorBoundary>
      </main>
    </div>
  );
}
