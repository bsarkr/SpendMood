import { format, startOfWeek, addDays, isSameDay } from 'date-fns';
import { useState, useEffect } from 'react';
import WeeklySummary from './WeeklySummary';
import PurchaseDetailModal from './PurchaseDetailModal';

const API_BASE = 'http://localhost:8000/api';

function CalendarView({ entries, onBack, user, onLogout }) {
    const [currentWeekStart, setCurrentWeekStart] = useState(startOfWeek(new Date()));
    const [weeklyPatterns, setWeeklyPatterns] = useState({ patterns: [], summary: '' });
    const [isLoadingPatterns, setIsLoadingPatterns] = useState(false);
    const [selectedEntry, setSelectedEntry] = useState(null);
    const [clickPosition, setClickPosition] = useState({ x: 0, y: 0 });

    const weekDays = Array.from({ length: 7 }, (_, i) => addDays(currentWeekStart, i));

    const getEntriesForDay = (day) => {
        return entries.filter(entry => isSameDay(new Date(entry.timestamp), day));
    };

    const weekEntries = entries.filter(entry => {
        const entryDate = new Date(entry.timestamp);
        return entryDate >= currentWeekStart && entryDate < addDays(currentWeekStart, 7);
    });

    // Fetch patterns from backend when week changes
    useEffect(() => {
        fetchWeeklyPatterns();
    }, [currentWeekStart]);

    const fetchWeeklyPatterns = async () => {
        if (weekEntries.length === 0) {
            setWeeklyPatterns({ patterns: [], summary: 'No data for this week.' });
            return;
        }

        setIsLoadingPatterns(true);
        try {
            // Use the end of the week as the target date
            const targetDate = addDays(currentWeekStart, 6).toISOString().split('T')[0];

            const response = await fetch(`${API_BASE}/patterns/summary`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: user?.sub || 'default_user',
                    date: targetDate
                })
            });

            if (response.ok) {
                const data = await response.json();
                setWeeklyPatterns(data);
            } else {
                // Fallback to simple calculation if backend fails
                const totalSpent = weekEntries.reduce((sum, e) => sum + e.amount, 0);
                const moodCounts = weekEntries.reduce((acc, e) => {
                    acc[e.mood] = (acc[e.mood] || 0) + 1;
                    return acc;
                }, {});
                const dominantMood = Object.keys(moodCounts).sort((a, b) => moodCounts[b] - moodCounts[a])[0];
                setWeeklyPatterns({
                    patterns: [],
                    summary: `You spent $${totalSpent.toFixed(2)} this week. Your mood was mostly ${dominantMood}.`
                });
            }
        } catch (error) {
            console.error('Error fetching weekly patterns:', error);
            setWeeklyPatterns({
                patterns: [],
                summary: 'Unable to analyze patterns at this time.'
            });
        } finally {
            setIsLoadingPatterns(false);
        }
    };

    const handleEntryClick = (entry, event) => {
        setClickPosition({ x: event.clientX, y: event.clientY });
        setSelectedEntry(entry);
    };

    return (
        <div className='content'>
            <div className="calendar-view">
                <div className="calendar-header">
                    <button className="back-btn" onClick={onBack}>← Log Your Spending</button>
                    <div className="user-info-calendar">
                        <span className="user-name">
                            {user?.username || user?.nickname || user?.given_name || user?.name?.split(' ')[0] || user?.email}
                        </span>
                        <button className="auth-btn logout-btn" onClick={onLogout}>
                            Log Out
                        </button>
                    </div>
                </div>

                <WeeklySummary
                    entries={weekEntries}
                    patterns={weeklyPatterns.patterns}
                    summary={weeklyPatterns.summary}
                    isLoading={isLoadingPatterns}
                />

                <div className="calendar-grid">
                    <div className="week-navigation">
                        <button onClick={() => setCurrentWeekStart(addDays(currentWeekStart, -7))}>
                            ← Previous Week
                        </button>
                        <h2>{format(currentWeekStart, 'MMM d')} - {format(addDays(currentWeekStart, 6), 'MMM d, yyyy')}</h2>
                        <button onClick={() => setCurrentWeekStart(addDays(currentWeekStart, 7))}>
                            Next Week →
                        </button>
                    </div>

                    <div className="days-grid">
                        {weekDays.map(day => {
                            const dayEntries = getEntriesForDay(day);
                            const isToday = isSameDay(day, new Date());

                            return (
                                <div key={day} className={`day-card ${isToday ? 'today' : ''}`}>
                                    <div className="day-header">
                                        <div className="day-name">{format(day, 'EEE')}</div>
                                        <div className="day-date">{format(day, 'd')}</div>
                                    </div>

                                    <div className="day-entries">
                                        {dayEntries.length === 0 ? (
                                            <div className="no-entries">
                                                <div className="no-entries-icon">📝</div>
                                                <div className="no-entries-text">No purchases logged</div>
                                            </div>
                                        ) : (
                                            dayEntries.map((entry, idx) => (
                                                <div
                                                    key={idx}
                                                    className="entry-item"
                                                    onClick={(e) => handleEntryClick(entry, e)}
                                                >
                                                    <div className={`mood-indicator mood-${entry.mood.toLowerCase()}`}>
                                                        {entry.mood}
                                                    </div>
                                                    <div className="entry-time">{format(new Date(entry.timestamp), 'h:mm a')}</div>
                                                    <div className="entry-purchase">${entry.amount} - {entry.item}</div>
                                                </div>
                                            ))
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {selectedEntry && (
                    <PurchaseDetailModal
                        entry={selectedEntry}
                        onClose={() => setSelectedEntry(null)}
                        position={clickPosition}
                    />
                )}
            </div>
        </div>
    );
}

export default CalendarView;