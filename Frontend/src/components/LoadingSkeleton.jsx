function LoadingSkeleton() {
    return (
        <div className="calendar-view">
            <div className="skeleton-header">
                <div className="skeleton-box" style={{ width: '120px', height: '40px' }}></div>
            </div>

            <div className="skeleton-summary">
                <div className="skeleton-box" style={{ width: '100%', height: '120px' }}></div>
            </div>

            <div className="days-grid">
                {[1, 2, 3, 4, 5, 6, 7].map(i => (
                    <div key={i} className="skeleton-day-card">
                        <div className="skeleton-box" style={{ width: '60px', height: '24px' }}></div>
                        <div className="skeleton-box" style={{ width: '100%', height: '80px', marginTop: '12px' }}></div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default LoadingSkeleton;