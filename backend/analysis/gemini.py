# backend/analysis/gemini.py

import json
import os
from typing import Tuple, Dict, Any
from dotenv import load_dotenv
from .prompts import GEMINI_PROMPT, PATTERN_ANALYSIS_PROMPT, SPENDING_EVALUATION_PROMPT

load_dotenv()

try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        print("Google Gemini client configured successfully.")
    else:
        model = None
        print("No GEMINI_API_KEY found in environment. Gemini will be disabled.")
except ImportError:
    genai = None
    model = None
    print("google.generativeai SDK not installed; Gemini will be disabled.")


def _detect_mood_from_text(text: str) -> Tuple[str, int]:
    """Simple fallback mood detector if Gemini isn't available."""
    t = text.lower()
    if any(w in t for w in ["sad", "depressed", "unhappy", "sucks", "terrible"]):
        return "sad", 1
    if any(w in t for w in ["angry", "mad", "furious"]):
        return "angry", 1
    if any(w in t for w in ["happy", "great", "joy", "awesome", "glad"]):
        return "happy", 5
    return "neutral", 3


def analyze_entry_with_gemini(text: str) -> dict:
    """
    Analyzes text using Gemini. Falls back to heuristic if unavailable.
    """
    if not model:
        print("WARNING: Gemini client not available. Using heuristic fallback.")
        label, rating = _detect_mood_from_text(text)
        return {"mood_label": label, "mood_rating": rating, "calculated_amount": None, "item": None}

    try:
        print(f"--- Calling Gemini API for: '{text}' ---")
        prompt = GEMINI_PROMPT.format(user_text=text)
        response = model.generate_content(prompt)
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        print(f"--- Gemini response: {response_text} ---")

        analysis = json.loads(response_text)

        required_keys = ["mood_label", "mood_rating",
                         "calculated_amount", "item"]
        if not all(key in analysis for key in required_keys):
            raise ValueError("Gemini response missing required keys.")

        return analysis

    except Exception as e:
        print(f"ERROR: Gemini call failed: {e}")
        label, rating = _detect_mood_from_text(text)
        return {"mood_label": label, "mood_rating": rating, "calculated_amount": None, "item": None}


def analyze_patterns_with_gemini(entries: list) -> dict:
    if not model:
        # Fallback: return empty patterns
        return {"patterns": [], "summary": "Gemini not available."}
    prompt = PATTERN_ANALYSIS_PROMPT.format(entries="\n".join(entries))
    response = model.generate_content(prompt)
    response_text = response.text.strip().replace("```json", "").replace("```", "")
    try:
        result = json.loads(response_text)
        # Ensure patterns are unique
        patterns = list({p.lower().strip(): p for p in result.get("patterns", [])}.values())
        result["patterns"] = patterns
        return result
    except Exception as e:
        return {"patterns": [], "summary": f"Gemini analysis failed: {e}"}


def analyze_spending_with_gemini(purchase_details: Dict[str, Any]) -> dict:
    """
    Analyzes a purchase for problematic spending patterns using Gemini.
    Falls back to conservative defaults if unavailable.
    """
    if not model:
        print("WARNING: Gemini client not available. Using conservative defaults.")
        # Default to not flagging as problematic when Gemini is unavailable
        return {
            "is_extreme": False,
            "confidence": 0.0,
            "reasons": [],
            "risk_factors": [],
            "recommendation": "Unable to analyze purchase at this time."
        }

    try:
        prompt = SPENDING_EVALUATION_PROMPT.format(purchase=json.dumps(purchase_details))
        response = model.generate_content(prompt)
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        print(f"--- Gemini spending analysis: {response_text} ---")
        
        analysis = json.loads(response_text)
        
        # Validate required fields
        required_keys = ["is_extreme", "confidence", "reasons", "risk_factors", "recommendation"]
        if not all(key in analysis for key in required_keys):
            raise ValueError("Gemini response missing required keys for spending analysis.")
            
        return analysis
        
    except Exception as e:
        print(f"ERROR: Gemini spending analysis failed: {e}")
        return {
            "is_extreme": False,
            "confidence": 0.0,
            "reasons": [],
            "risk_factors": [],
            "recommendation": f"Analysis failed: {str(e)}"
        }