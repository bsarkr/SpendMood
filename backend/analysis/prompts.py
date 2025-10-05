# By Chloe Velez, Yuki Li, Bilash Sarkar
# 10-05-2025

PATTERN_ANALYSIS_PROMPT = """
You are an expert behavioral analyst for a personal finance app.
Given a list of user mood logs and purchase reasons from the past 7 days, identify unique behavioral patterns.
For example: 'buys ice cream when sad', 'spends more on weekends', 'shops online when stressed'.


Return ONLY a valid JSON object with:
{{
  "patterns": [list of unique, non-similar conclusions as strings],
  "summary": "A short summary of the user's recent behavioral patterns."
}}

Entries:
{{entries}}

Example Output:
{{
  "patterns": [
    "You tend to buy ice cream when you feel sad.",
    "You spend more on weekends.",
    "You shop online when stressed."
  ],
  "summary": "Recently, your spending increases on weekends and you often buy ice cream when feeling sad."
}}

Entries:
- "I bought coffee every morning before work."
- "I felt anxious and ordered takeout."
- "Spent $50 on video games when bored."
- "Went shopping online late at night."
- "Bought snacks after a stressful meeting."

Your Output:
{{
  "patterns": [
    "You tend to buy coffee every morning before work.",
    "You order takeout when feeling anxious.",
    "You spend more on video games when bored.",
    "You shop online late at night.",
    "You buy snacks after stressful meetings."
  ],
  "summary": "Your recent patterns include morning coffee purchases, late-night shopping, and stress-related snacking."
}}

Entries:
- "Bought lunch with coworkers on Friday."
- "Spent extra on groceries when feeling tired."
- "Purchased a book after reading a positive review."
- "Bought ice cream after a long day."
- "Spent more on entertainment during the weekend."

Your Output:
{{
  "patterns": [
    "You tend to buy lunch with coworkers on Fridays.",
    "You spend extra on groceries when tired.",
    "You buy books after reading positive reviews.",
    "You buy ice cream after long days.",
    "You spend more on entertainment during weekends."
  ],
  "summary": "You often spend more on weekends, buy ice cream after long days, and make purchases influenced by positive reviews."
}}
"""
# backend/analysis/prompts.py

GEMINI_PROMPT = """
You are an expert financial and emotional analyst for a mindfulness app.
Your task is to analyze a user's free-text journal entry and extract structured data.

Analyze the following user entry:
"{user_text}"

Based on the text, perform these actions:
1.  Determine the primary mood. Choose ONLY from: "happy", "sad", "angry", "neutral".
2.  Assign a mood rating on a scale of 1 (very negative) to 5 (very positive).
3.  If a purchase is mentioned, identify the item(s).
4.  Calculate the total transaction amount. If a quantity and price are mentioned (e.g., "17 $7 redbulls"), multiply them to get the total. If no amount is mentioned, this should be null.

Return ONLY a valid JSON object with the following schema:
{{
  "mood_label": string,
  "mood_rating": integer,
  "calculated_amount": float or null,
  "item": string or null
}}

Here are some examples:

- User Entry: "bought 17 $7 redbulls and I am so happy"
- Your Output:
{{
  "mood_label": "happy",
  "mood_rating": 5,
  "calculated_amount": 119.0,
  "item": "redbulls"
}}

- User Entry: "had a terrible day at work, this sucks. bought a book to feel better"
- Your Output:
{{
  "mood_label": "sad",
  "mood_rating": 2,
  "calculated_amount": null,
  "item": "book"
}}

- User Entry: "Just refilled my metrocard for the week."
- Your Output:
{{
  "mood_label": "neutral",
  "mood_rating": 3,
  "calculated_amount": null,
  "item": "metrocard"
}}
"""

PATTERN_ANALYSIS_PROMPT = """
You are an expert behavioral analyst for a personal finance app.
Given a list of user mood logs and purchase reasons from the past 7 days, identify unique behavioral patterns.
For example: 'buys ice cream when sad', 'spends more on weekends', 'shops online when stressed'.

Return ONLY a valid JSON object with:
{{
  "patterns": [list of unique, non-similar conclusions as strings],
  "summary": "A short summary of the user's recent behavioral patterns."
}}

Entries:
{entries}

Here are some examples:

Entries:
- "I felt sad and bought ice cream."
- "I was stressed and bought a book."
- "I was happy and went out for dinner."
- "Bought ice cream again when feeling down."
- "Spent more money on Saturday."

Your Output:
{{
  "patterns": [
    "You tend to buy ice cream when you feel sad.",
    "You spend more on weekends.",
    "You shop online when stressed."
  ],
  "summary": "Recently, your spending increases on weekends and you often buy ice cream when feeling sad."
}}
"""

SPENDING_EVALUATION_PROMPT = """
You are an expert financial and emotional analyst for a personal finance app.
Given details about a purchase, evaluate if the spending behavior may be problematic
and whether intervention might be helpful.

Analyze this purchase:
{{purchase}}

Return ONLY a valid JSON object with:
{{
  "is_extreme": boolean,   // Whether this could be problematic spending
  "confidence": float,    // 0.0-1.0 how confident you are in the analysis
  "reasons": [string],    // List of reasons why this may be concerning
  "risk_factors": [string],  // Specific behaviors that increase risk
  "recommendation": string  // A gentle suggestion for the user
}}

Example:

Purchase details:
{{
  "amount": 199.99,
  "description": "Online shopping spree at 2am",
  "mood": "stressed"
}}

Example Output:
{{
  "is_extreme": true,
  "confidence": 0.85,
  "reasons": [
    "Large impulse purchase late at night",
    "Spending while in a stressed emotional state",
    "Online shopping which can be more impulsive"
  ],
  "risk_factors": [
    "Late night shopping",
    "Emotional spending",
    "High amount for single purchase"
  ],
  "recommendation": "Consider implementing a 24-hour rule for purchases over $100, especially late at night."
}}

Analyze based on factors like:
- Time of purchase
- Amount relative to typical spending
- Emotional state  
- Purchase medium (online vs in-store)
- Urgency/necessity
- Pattern matching to known risky behaviors

Focus on being supportive and non-judgmental in recommendations.
"""
