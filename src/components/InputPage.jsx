import { useState, useEffect } from 'react';
import { parseEntry } from '../utils/langchain';

function InputPage({ onSubmit, hasEntries, onViewCalendar, isAuthenticated, user, onLogin, onLogout, pendingInput, setPendingInput }) {
    const [input, setInput] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);

    // Auto-submit pending input after login
    useEffect(() => {
        if (pendingInput && isAuthenticated) {
            setInput(pendingInput);
            handleSubmitPending(pendingInput);
        }
    }, [pendingInput, isAuthenticated]);

    const handleSubmitPending = async (text) => {
        setIsProcessing(true);
        try {
            const parsedData = await parseEntry(text);
            onSubmit(parsedData, text);
            setInput('');
            setPendingInput('');
        } catch (error) {
            console.error('Error parsing entry:', error);
            alert('Error processing your entry. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        if (!isAuthenticated) {
            // Will save input and redirect
            onSubmit(null, input);
            return;
        }

        setIsProcessing(true);

        try {
            const parsedData = await parseEntry(input);
            onSubmit(parsedData, input);
            setInput('');
        } catch (error) {
            console.error('Error parsing entry:', error);
            alert('Error processing your entry. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="input-page">
            <div className="auth-header">
                {isAuthenticated ? (
                    <div className="user-info">
                        <span className="user-name">
                            Welcome, {user?.given_name || user?.name?.split(' ')[0] || 'there'}
                        </span>
                        <button className="auth-btn logout-btn" onClick={onLogout}>
                            Log Out
                        </button>
                    </div>
                ) : (
                    <button className="auth-btn login-btn" onClick={onLogin}>
                        Log In
                    </button>
                )}
            </div>

            <div className="input-container">
                <h1 className="app-title">Track Your Spending and Mood!</h1>
                <p className="subtitle">Understanding the connection between how you feel and what you buy</p>

                <form onSubmit={handleSubmit}>
                    <textarea
                        className="mood-input"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="What did you buy today? How much did it cost? How are you feeling?"
                        rows={6}
                        disabled={isProcessing}
                    />

                    <button
                        type="submit"
                        className="submit-btn"
                        disabled={isProcessing || !input.trim()}
                    >
                        {isProcessing ? 'Processing...' : (isAuthenticated ? 'Log Entry' : 'Log Entry (Login Required)')}
                    </button>
                </form>

                {hasEntries && isAuthenticated && (
                    <button className="view-calendar-btn" onClick={onViewCalendar}>
                        View Calendar
                    </button>
                )}
            </div>

            <div className="hint-text">
                Example: "Feeling stressed after work. Bought a $45 shirt from H&M at 9pm to feel better."
            </div>
        </div>
    );
}

export default InputPage;