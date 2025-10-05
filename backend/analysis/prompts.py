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