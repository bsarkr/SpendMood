import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

function WeeklySummary({ entries, insight }) {
    const totalSpent = entries.reduce((sum, e) => sum + e.amount, 0);
    const moodCounts = entries.reduce((acc, e) => {
        acc[e.mood] = (acc[e.mood] || 0) + 1;
        return acc;
    }, {});

    // Prepare data for chart
    const moodColors = {
        'Happy': '#28a745',
        'Stressed': '#dc3545',
        'Sad': '#17a2b8',
        'Anxious': '#ffc107',
        'Neutral': '#6c757d'
    };

    const chartData = Object.entries(moodCounts).map(([mood, count]) => ({
        mood,
        purchases: count,
        color: moodColors[mood]
    }));

    return (
        <div className="weekly-summary">
            <h3>Your Week</h3>

            <div className="summary-grid">
                <div className="summary-card">
                    <div className="stat-label">Total Spent</div>
                    <div className="stat-value">${totalSpent.toFixed(2)}</div>
                </div>

                <div className="summary-card">
                    <div className="stat-label">Purchases</div>
                    <div className="stat-value">{entries.length}</div>
                </div>

                <div className="summary-card chart-card">
                    <div className="stat-label">Mood Distribution</div>
                    {chartData.length > 0 && (
                        <ResponsiveContainer width="100%" height={120}>
                            <BarChart data={chartData}>
                                <XAxis dataKey="mood" tick={{ fontSize: 12 }} />
                                <YAxis tick={{ fontSize: 12 }} />
                                <Tooltip />
                                <Bar dataKey="purchases" radius={[8, 8, 0, 0]}>
                                    {chartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {insight && (
                <div className="insight-box">
                    <strong>💡 Insight:</strong> {insight}
                </div>
            )}
        </div>
    );
}

export default WeeklySummary;