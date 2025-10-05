import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import InputPage from './components/InputPage';
import CalendarView from './components/CalendarView';
import './App.css';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const { isAuthenticated, isLoading, loginWithRedirect, logout, user } = useAuth0();
  const [view, setView] = useState('input');
  const [entries, setEntries] = useState([]);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [pendingInput, setPendingInput] = useState('');

  // Load entries from backend when authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchEntriesFromBackend();
    }
  }, [isAuthenticated, user]);

  const fetchEntriesFromBackend = async () => {
    try {
      const response = await fetch(`${API_BASE}/mockdb`);
      const data = await response.json();

      // Convert backend transactions to frontend format
      const backendEntries = Object.values(data.transactions).map(tx => ({
        timestamp: tx.timestamp,
        mood: 'Neutral', // Default, could enhance this
        amount: tx.amount,
        item: tx.merchant,
        reason: `Purchased from ${tx.merchant}`,
        category: 'Shopping'
      }));

      setEntries(backendEntries);
    } catch (error) {
      console.error('Failed to fetch entries from backend:', error);
    }
  };

  useEffect(() => {
    const pending = sessionStorage.getItem('pending_entry');
    if (pending && isAuthenticated) {
      setPendingInput(pending);
      sessionStorage.removeItem('pending_entry');
    }
  }, [isAuthenticated]);

  const handleEntrySubmit = async (parsedData, inputText) => {
    if (!isAuthenticated) {
      sessionStorage.setItem('pending_entry', inputText);
      loginWithRedirect();
      return;
    }

    setIsTransitioning(true);
    setEntries(prev => [...prev, parsedData]);

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
    if (!isAuthenticated) {
      loginWithRedirect();
    } else {
      fetchEntriesFromBackend(); // Refresh before viewing
      setIsTransitioning(true);
      setTimeout(() => {
        setView('calendar');
        setIsTransitioning(false);
      }, 300);
    }
  };

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className={`app ${isTransitioning ? 'transitioning' : ''}`}>
      {view === 'input' ? (
        <InputPage
          onSubmit={handleEntrySubmit}
          hasEntries={entries.length > 0}
          onViewCalendar={handleViewCalendar}
          isAuthenticated={isAuthenticated}
          user={user}
          onLogin={loginWithRedirect}
          onLogout={() => logout({ logoutParams: { returnTo: window.location.origin } })}
          pendingInput={pendingInput}
          setPendingInput={setPendingInput}
        />
      ) : (
        <CalendarView
          entries={entries}
          onBack={handleBackToInput}
          user={user}
          onLogout={() => logout({ logoutParams: { returnTo: window.location.origin } })}
        />
      )}
    </div>
  );
}

export default App;