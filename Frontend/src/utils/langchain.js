// This is where your LangGraph agents live

export async function parseEntry(inputText) {
    // TODO: Implement LangGraph agent pipeline
    // Agent 1: Extract structured data from natural language
    // Agent 2: Categorize mood
    // Agent 3: Identify purchase details

    // For now, mock response
    // Replace this with actual LangChain/LangGraph calls

    const mockParsed = {
        timestamp: new Date().toISOString(),
        mood: detectMood(inputText), // "Happy", "Stressed", "Sad", "Neutral", "Anxious"
        amount: extractAmount(inputText),
        item: extractItem(inputText),
        reason: inputText,
        category: "Shopping" // Could be: Shopping, Food, Entertainment, etc.
    };

    return mockParsed;
}

function detectMood(text) {
    const lower = text.toLowerCase();
    if (lower.includes('stress') || lower.includes('rough') || lower.includes('bad')) return 'Stressed';
    if (lower.includes('happy') || lower.includes('great') || lower.includes('good')) return 'Happy';
    if (lower.includes('sad') || lower.includes('down') || lower.includes('depressed')) return 'Sad';
    if (lower.includes('anxious') || lower.includes('worried') || lower.includes('nervous')) return 'Anxious';
    return 'Neutral';
}

function extractAmount(text) {
    const match = text.match(/\$?(\d+(?:\.\d{2})?)/);
    return match ? parseFloat(match[1]) : 0;
}

function extractItem(text) {
    // Simple extraction - improve with LLM
    const words = text.split(' ');
    const boughtIndex = words.findIndex(w => w.toLowerCase().includes('bought') || w.toLowerCase().includes('buy'));
    if (boughtIndex !== -1 && boughtIndex < words.length - 1) {
        return words.slice(boughtIndex + 1, boughtIndex + 4).join(' ');
    }
    return 'Item';
}

export async function analyzeWeeklyPattern(entries) {
    // TODO: LangGraph Agent 4: Pattern analysis
    // Correlate mood with spending
    // Identify triggers
    // Generate insights

    return "Pattern analysis insight here";
}