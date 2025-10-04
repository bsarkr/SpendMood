import { useState } from 'react';
import InputPage from './components/InputPage';
import CalendarView from './components/CalendarView';
import './App.css';

function App() {
  const [view, setView] = useState('input'); // 'input' or 'calendar'
  const [entries, setEntries] = useState([]);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleEntrySubmit = async (parsedData) => {
    setIsTransitioning(true);

    // Add new entry
    setEntries(prev => [...prev, parsedData]);

    // Smooth transition after 300ms
    setTimeout(() => {
      setView('calendar');
      setIsTransitioning(false);
    }, 300);
  };

  const handleBackToInput = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setView('input');
      setIsTransitioning(false);
    }, 300);
  };

  const handleViewCalendar = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setView('calendar');
      setIsTransitioning(false);
    }, 300);
  };

  return (
    <div className={`app ${isTransitioning ? 'transitioning' : ''}`}>
      {view === 'input' ? (
        <InputPage onSubmit={handleEntrySubmit} hasEntries={entries.length > 0} onViewCalendar={handleViewCalendar} />
      ) : (
        <CalendarView entries={entries} onBack={handleBackToInput} />
      )}
    </div>
  );
}

export default App;