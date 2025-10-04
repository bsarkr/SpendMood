import { useState } from 'react';
import { parseEntry } from '../utils/langchain';

function InputPage({ onSubmit, hasEntries, onViewCalendar }) {
    const [input, setInput] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        setIsProcessing(true);

        try {
            // Call LangChain agent to parse the input
            const parsedData = await parseEntry(input);
            onSubmit(parsedData);
            setInput('');
        } catch (error) {
            console.error('Error parsing entry:', error);
            alert('Error processing your entry. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className = "content">
            <div className="input-page">
                <div className="input-container">
                    <h1 className="app-title">How was your day?</h1>

                    <form onSubmit={handleSubmit}>
                        <textarea
                            className="mood-input"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Tell me about your day... What did you buy? How are you feeling?"
                            rows={6}
                            disabled={isProcessing}
                        />

                        <button
                            type="submit"
                            className="submit-btn"
                            disabled={isProcessing || !input.trim()}
                        >
                            {isProcessing ? 'Processing...' : 'Log Entry'}
                        </button>
                    </form>

                    {hasEntries && (
                        <button className="view-calendar-btn" onClick={onViewCalendar}>
                            View Calendar
                        </button>
                    )}
                </div>

                <div className="hint-text">
                    Example: "Had a rough day at work. Feeling stressed. Bought a $45 shirt from H&M at 9pm to cheer myself up."
                </div>
            </div>
        </div>
    );
}

export default InputPage;