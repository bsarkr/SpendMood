import { format, startOfWeek, addDays, isSameDay } from 'date-fns';
import { useState, useEffect } from 'react';
import WeeklySummary from './WeeklySummary';
import PurchaseDetailModal from './PurchaseDetailModal';

function CalendarView({ entries, onBack, user, onLogout }) {
    const [currentWeekStart, setCurrentWeekStart] = useState(startOfWeek(new Date()));
    const [weeklyInsight, setWeeklyInsight] = useState('');
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

    useEffect(() => {
        if (weekEntries.length > 0) {
            generateWeeklyInsight(weekEntries).then(setWeeklyInsight);
        }
    }, [weekEntries]);

    const handleEntryClick = (entry, event) => {
        setClickPosition({ x: event.clientX, y: event.clientY });
        setSelectedEntry(entry);
    };

    return (
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

            <WeeklySummary entries={weekEntries} insight={weeklyInsight} />

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
    );
}

async function generateWeeklyInsight(entries) {
    const totalSpent = entries.reduce((sum, e) => sum + e.amount, 0);
    const avgMood = entries.length > 0 ? 'mixed' : 'neutral';
    return `You spent $${totalSpent.toFixed(2)} this week. Your mood was ${avgMood}.`;
}

export default CalendarView;