function WeeklySummary({ entries, patterns, summary, isLoading }) {
    const totalSpent = entries.reduce((sum, e) => sum + e.amount, 0);

    const moodCounts = entries.reduce((acc, e) => {
        acc[e.mood] = (acc[e.mood] || 0) + 1;
        return acc;
    }, {});

    const avgSpending = entries.length > 0 ? totalSpent / entries.length : 0;

    return (
        <div className="weekly-summary">
            <h3>Weekly Overview</h3>

            <div className="summary-grid">
                <div className="summary-card">
                    <div className="stat">
                        <div className="stat-label">Total Spent</div>
                        <div className="stat-value">${totalSpent.toFixed(2)}</div>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="stat">
                        <div className="stat-label">Transactions</div>
                        <div className="stat-value">{entries.length}</div>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="stat">
                        <div className="stat-label">Avg per Purchase</div>
                        <div className="stat-value">${avgSpending.toFixed(2)}</div>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="stat">
                        <div className="stat-label">Mood Breakdown</div>
                        <div className="mood-pills">
                            {Object.entries(moodCounts).map(([mood, count]) => (
                                <span key={mood} className={`mood-pill mood-${mood.toLowerCase()}`}>
                                    {mood}: {count}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {isLoading ? (
                <div className="insight-box">
                    <div className="skeleton-box" style={{ height: '60px', width: '100%' }}></div>
                </div>
            ) : (
                <>
                    {summary && (
                        <div className="insight-box">
                            <strong>💡 AI Insights:</strong> {summary}
                        </div>
                    )}

                    {patterns && patterns.length > 0 && (
                        <div className="patterns-section">
                            <h4 style={{ marginTop: '1.5rem', marginBottom: '1rem', color: '#667eea' }}>
                                Behavioral Patterns Detected
                            </h4>
                            <ul className="patterns-list">
                                {patterns.map((pattern, idx) => (
                                    <li key={idx} className="pattern-item">
                                        {pattern}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default WeeklySummary;