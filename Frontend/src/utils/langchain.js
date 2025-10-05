// src/utils/langchain.js

const API_BASE = 'http://localhost:8000/api';

export async function parseEntry(inputText) {
    try {
        // Extract amount from text
        const amountMatch = inputText.match(/\$?(\d+(?:\.\d{2})?)/);
        const amount = amountMatch ? parseFloat(amountMatch[1]) : null;

        // Call backend /api/log endpoint
        const response = await fetch(`${API_BASE}/log`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: inputText,
                amount: amount,
                timestamp: new Date().toISOString()
            })
        });

        if (!response.ok) {
            throw new Error('Backend request failed');
        }

        const data = await response.json();

        // Transform backend response to frontend format
        return {
            timestamp: new Date().toISOString(),
            mood: capitalizeFirst(data.mood?.label || 'Neutral'),
            amount: data.transaction?.amount || amount || 0,
            item: extractItem(inputText),
            reason: inputText,
            category: guessCategory(inputText)
        };
    } catch (error) {
        console.error('Error calling backend:', error);
        // Fallback to local parsing if backend fails
        return {
            timestamp: new Date().toISOString(),
            mood: detectMoodLocal(inputText),
            amount: extractAmount(inputText),
            item: extractItem(inputText),
            reason: inputText,
            category: guessCategory(inputText)
        };
    }
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function extractItem(text) {
    const words = text.split(' ');
    const boughtIndex = words.findIndex(w =>
        w.toLowerCase().includes('bought') ||
        w.toLowerCase().includes('buy') ||
        w.toLowerCase().includes('purchased')
    );
    if (boughtIndex !== -1 && boughtIndex < words.length - 1) {
        return words.slice(boughtIndex + 1, Math.min(boughtIndex + 4, words.length)).join(' ');
    }
    return 'Item';
}

function guessCategory(text) {
    const lower = text.toLowerCase();
    if (lower.includes('food') || lower.includes('restaurant') || lower.includes('coffee') || lower.includes('lunch') || lower.includes('dinner')) return 'Food';
    if (lower.includes('shirt') || lower.includes('clothes') || lower.includes('fashion') || lower.includes('dress')) return 'Shopping';
    if (lower.includes('gas') || lower.includes('uber') || lower.includes('lyft') || lower.includes('taxi')) return 'Transportation';
    if (lower.includes('movie') || lower.includes('concert') || lower.includes('show')) return 'Entertainment';
    return 'Shopping';
}

function extractAmount(text) {
    const match = text.match(/\$?(\d+(?:\.\d{2})?)/);
    return match ? parseFloat(match[1]) : 0;
}

function detectMoodLocal(text) {
    const lower = text.toLowerCase();
    if (lower.includes('stress') || lower.includes('rough') || lower.includes('bad') || lower.includes('terrible')) return 'Stressed';
    if (lower.includes('happy') || lower.includes('great') || lower.includes('good') || lower.includes('excited')) return 'Happy';
    if (lower.includes('sad') || lower.includes('down') || lower.includes('depressed')) return 'Sad';
    if (lower.includes('anxious') || lower.includes('worried') || lower.includes('nervous')) return 'Anxious';
    return 'Neutral';
}

export async function analyzeWeeklyPattern(entries) {
    // TODO: Call backend for AI-generated insights
    const totalSpent = entries.reduce((sum, e) => sum + e.amount, 0);
    const moodCounts = entries.reduce((acc, e) => {
        acc[e.mood] = (acc[e.mood] || 0) + 1;
        return acc;
    }, {});
    const dominantMood = Object.keys(moodCounts).sort((a, b) => moodCounts[b] - moodCounts[a])[0] || 'neutral';
    return `You spent $${totalSpent.toFixed(2)} this week. Your mood was mostly ${dominantMood}.`;
}