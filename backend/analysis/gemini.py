# """
# backend/analysis/gemini.py

# Defensive wrapper around Google Gemini / Generative AI usage.
# If the official `google.generativeai` package isn't installed or cannot be
# configured, the module falls back to a small heuristic detector so the
# rest of the backend continues to work in dev environments.
# """


# import json
# import os
# from typing import Tuple, Optional
# from dotenv import load_dotenv

# # Load .env (so GEMINI_API_KEY placed in backend/.env will be found)
# load_dotenv()

# try:
#     # The recommended package is `google.generativeai` (imported as genai)
#     import google.generativeai as genai
# except Exception:
#     genai = None

# from .prompts import GEMINI_PROMPT


# def _detect_mood_from_text(text: str) -> Tuple[str, int]:
#     """Simple fallback mood detector if Gemini isn't available."""
#     t = text.lower()
#     if any(w in t for w in ["sad", "depressed", "unhappy", "sucks", "terrible"]):
#         return "sad", 1
#     if any(w in t for w in ["angry", "mad", "furious"]):
#         return "angry", 1
#     if any(w in t for w in ["happy", "great", "joy", "awesome"]):
#         return "happy", 5
#     return "neutral", 3


# def analyze_entry_with_gemini(text: str) -> dict:
#     """Attempt to analyze `text` using Gemini. Returns a dict with keys:
#     - mood_label (str)
#     - mood_rating (int)
#     - calculated_amount (float | None)
#     - item (str | None)

#     If Gemini is unavailable or any error occurs, we return a best-effort
#     heuristic result so the backend remains usable in development.
#     """

#     # If the SDK isn't available, fallback immediately
#     if genai is None:
#         print("google.generativeai SDK not installed; using heuristic fallback.")
#         label, rating = _detect_mood_from_text(text)
#         return {
#             "mood_label": label,
#             "mood_rating": rating,
#             "calculated_amount": None,
#             "item": None,
#         }

#     # Configure the client if an API key is present in env (load_dotenv called above)
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         print("No GOOGLE_API_KEY/GEMINI_API_KEY found in environment; falling back to heuristic detector.")
#         label, rating = _detect_mood_from_text(text)
#         return {
#             "mood_label": label,
#             "mood_rating": rating,
#             "calculated_amount": None,
#             "item": None,
#         }

#     # Try to configure the SDK with the provided API key
#     try:
#         genai.configure(api_key=api_key)
#         print("Google Gemini client configured successfully using environment key.")
#     except Exception:
#         # Some SDK versions may require env var; set and continue
#         os.environ["GOOGLE_API_KEY"] = api_key
#         print("Configured GOOGLE_API_KEY environment variable for Gemini SDK.")

#     try:
#         # Safe configure (API can be configured multiple ways across SDK versions)
#         try:
#             genai.configure(api_key=api_key)
#         except Exception:
#             # Some SDK versions accept setting env var instead
#             os.environ["GOOGLE_API_KEY"] = api_key

#         # Build the prompt and call the model. Different SDK versions use
#         # different method names; guard for common signatures.
#         prompt = GEMINI_PROMPT.format(user_text=text)

#         # Try multiple possible SDK call patterns to be resilient across
#         # different `google.generativeai` versions.
#         model_name = "gemini-2.5-flash"

#         def _extract_text_from_response(resp) -> str:
#             # Common response shapes: object with .text, dict with 'candidates'/'output',
#             # or string representation. Try several heuristics.
#             if resp is None:
#                 return ""
#             # direct attribute
#             if hasattr(resp, "text") and resp.text:
#                 return resp.text
#             # some SDKs return a dict-like object
#             try:
#                 # dict-like
#                 if isinstance(resp, dict):
#                     # candidates -> first -> content/text
#                     if "candidates" in resp and resp["candidates"]:
#                         c = resp["candidates"][0]
#                         if isinstance(c, dict):
#                             return c.get("content") or c.get("text") or str(c)
#                         return str(c)
#                     if "output" in resp and resp["output"]:
#                         out = resp["output"]
#                         if isinstance(out, list) and out:
#                             first = out[0]
#                             if isinstance(first, dict):
#                                 return first.get("content") or first.get("text") or str(first)
#                             return str(first)
#                     # direct content
#                     if "content" in resp:
#                         return resp["content"]
#                 # objects with attributes
#                 if hasattr(resp, "candidates"):
#                     c = getattr(resp, "candidates")
#                     if c:
#                         first = c[0]
#                         if hasattr(first, "content"):
#                             return getattr(first, "content")
#                         if isinstance(first, dict):
#                             return first.get("content") or first.get("text") or str(first)
#                 if hasattr(resp, "output"):
#                     out = getattr(resp, "output")
#                     if out:
#                         first = out[0]
#                         if hasattr(first, "content"):
#                             return getattr(first, "content")
#                         if isinstance(first, dict):
#                             return first.get("content") or first.get("text") or str(first)
#             except Exception:
#                 pass
#             # fallback to string
#             try:
#                 return str(resp)
#             except Exception:
#                 return ""

#         tried = []
#         response_text = ""

#         # Candidate callables in order of preference
#         callables = []
#         if hasattr(genai, "Client"):
#             def _client_generate():
#                 client = genai.Client()
#                 # try a few client method names
#                 if hasattr(client, "generate_text"):
#                     return client.generate_text(model=model_name, prompt=prompt)
#                 if hasattr(client, "generate"):
#                     return client.generate(model=model_name, prompt=prompt)
#                 if hasattr(client, "generate_message"):
#                     return client.generate_message(model=model_name, prompt=prompt)
#                 # last resort: try a generic call
#                 return client.generate(prompt=prompt, model=model_name)

#             callables.append((_client_generate, "Client.generate/_generate_text"))

#         # Module-level helpers
#         if hasattr(genai, "generate_text"):
#             callables.append((lambda: genai.generate_text(model=model_name, prompt=prompt), "genai.generate_text"))
#         if hasattr(genai, "generate"):
#             callables.append((lambda: genai.generate(model=model_name, prompt=prompt), "genai.generate"))
#         if hasattr(genai, "generate_content"):
#             callables.append((lambda: genai.generate_content(prompt), "genai.generate_content"))
#         if hasattr(genai, "responses") and hasattr(genai.responses, "generate"):
#             callables.append((lambda: genai.responses.generate(model=model_name, prompt=prompt), "genai.responses.generate"))
#         if hasattr(genai, "chat") and hasattr(genai.chat, "generate"):
#             callables.append((lambda: genai.chat.generate(model=model_name, messages=[{"content": prompt}]), "genai.chat.generate"))

#         # Try each callable until one succeeds
#         last_exc = None
#         for fn, name in callables:
#             try:
#                 tried.append(name)
#                 resp = fn()
#                 response_text = _extract_text_from_response(resp)
#                 if response_text:
#                     break
#             except Exception as e:
#                 last_exc = e

#         if not response_text:
#             # Instead of raising, print a diagnostic of available attributes and
#             # fall back to the heuristic detector so the server remains usable.
#             try:
#                 available = sorted([n for n in dir(genai) if not n.startswith("__")])
#             except Exception:
#                 available = [str(type(genai))]
#             print(
#                 "No supported generation method found on google.generativeai SDK."
#                 f" Tried: {tried}. Last error: {last_exc}. Available attributes: {available}"
#             )
#             label, rating = _detect_mood_from_text(text)
#             return {
#                 "mood_label": label,
#                 "mood_rating": rating,
#                 "calculated_amount": None,
#                 "item": None,
#             }

#         # Clean up and parse JSON
#         response_text = response_text.strip().replace("```json", "").replace("```", "")
#         analysis = json.loads(response_text)

#         # Ensure required keys exist
#         required_keys = ["mood_label", "mood_rating", "calculated_amount", "item"]
#         if not all(k in analysis for k in required_keys):
#             raise ValueError("Gemini response missing required keys")

#         return analysis

#     except Exception as e:
#         print(f"Gemini call failed or returned unexpected output: {e}")
#         label, rating = _detect_mood_from_text(text)
#         return {
#             "mood_label": label,
#             "mood_rating": rating,
#             "calculated_amount": None,
#             "item": None,
#         }

# backend/analysis/gemini.py

import json
import os
from typing import Tuple
from dotenv import load_dotenv
from .prompts import GEMINI_PROMPT

# Load .env (so GEMINI_API_KEY placed in backend/.env will be found)
load_dotenv()

try:
    import google.generativeai as genai
    # --- SIMPLIFIED: Configure the SDK once at the start ---
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        # print("Available models:")
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(m.name)
        # --- SIMPLIFIED: Get the model once ---
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
    if any(w in t for w in ["happy", "great", "joy", "awesome"]):
        return "happy", 5
    return "neutral", 3


def analyze_entry_with_gemini(text: str) -> dict:
    """
    Analyzes `text` using the configured Gemini model.
    Falls back to a simple heuristic if the model is unavailable or fails.
    """
    # If the model failed to initialize, fallback immediately
    if not model:
        print("WARNING: Gemini client not available. Using heuristic fallback.")
        label, rating = _detect_mood_from_text(text)
        return {"mood_label": label, "mood_rating": rating, "calculated_amount": None, "item": None}

    try:
        print("--- Calling Gemini API ---")
        prompt = GEMINI_PROMPT.format(user_text=text)

        # --- SIMPLIFIED: The only API call you need ---
        response = model.generate_content(prompt)

        # The response object has a simple .text attribute.
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        analysis = json.loads(response_text)

        # Validate the output to ensure it matches the schema
        required_keys = ["mood_label", "mood_rating", "calculated_amount", "item"]
        if not all(key in analysis for key in required_keys):
            raise ValueError("Gemini response missing required keys.")

        return analysis

    except Exception as e:
        print(f"ERROR: Gemini call failed or returned unexpected output: {e}")
        # Fallback in case of any API error
        label, rating = _detect_mood_from_text(text)
        return {"mood_label": label, "mood_rating": rating, "calculated_amount": None, "item": None}