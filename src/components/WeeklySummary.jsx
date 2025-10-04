function WeeklySummary({ entries, insight }) {
    const totalSpent = entries.reduce((sum, e) => sum + e.amount, 0);
    const moodCounts = entries.reduce((acc, e) => {
        acc[e.mood] = (acc[e.mood] || 0) + 1;
        return acc;
    }, {});

    return (
        <div className="weekly-summary">
            <h3>Your Week</h3>
            <div className="summary-stats">
                <div className="stat">
                    <span className="stat-label">Total Spent</span>
                    <span className="stat-value">${totalSpent.toFixed(2)}</span>
                </div>
                <div className="stat">
                    <span className="stat-label">Entries</span>
                    <span className="stat-value">{entries.length}</span>
                </div>
                <div className="stat">
                    <span className="stat-label">Mood Distribution</span>
                    <div className="mood-pills">
                        {Object.entries(moodCounts).map(([mood, count]) => (
                            <span key={mood} className={`mood-pill mood-${mood.toLowerCase()}`}>
                                {mood}: {count}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            {insight && (
                <div className="insight-box">
                    <strong>Insight:</strong> {insight}
                </div>
            )}
        </div>
    );
}

export default WeeklySummary;