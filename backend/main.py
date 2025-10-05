from analysis.gemini import analyze_entry_with_gemini, analyze_patterns_with_gemini
from pydantic import BaseModel
from datetime import timedelta

# backend/main.py
import json
import uuid
import requests
import os
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import TypedDict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
try:
    from .analysis.gemini import analyze_entry_with_gemini
except Exception:
    try:
        from analysis.gemini import analyze_entry_with_gemini
    except Exception:
        import importlib.util
        import sys

        gemini_path = Path(__file__).parent / "analysis" / "gemini.py"
        spec = importlib.util.spec_from_file_location(
            "analysis.gemini", str(gemini_path))
        gemini_mod = importlib.util.module_from_spec(spec)
        sys.modules["analysis.gemini"] = gemini_mod
        spec.loader.exec_module(gemini_mod)
        analyze_entry_with_gemini = getattr(
            gemini_mod, "analyze_entry_with_gemini")
from dotenv import load_dotenv

load_dotenv()
NESSIE_API_KEY = os.getenv("SECRET_NESSIE")
NESSIE_BASE_URL = "http://api.nessieisreal.com"


class LogPayload(BaseModel):
    text: str
    amount: Optional[float] = None
    timestamp: Optional[str] = None


DB_PATH = Path(__file__).parent / "mock_db.json"


def _deserialize_db(raw: dict) -> dict:
    db = raw.copy()
    txs = {}
    for k, v in db.get("transactions", {}).items():
        tx = v.copy()
        ts = tx.get("timestamp")
        if isinstance(ts, str):
            try:
                tx["timestamp"] = datetime.fromisoformat(ts)
            except Exception:
                tx["timestamp"] = datetime.now()
        txs[k] = tx
    db["transactions"] = txs

    mood_logs = {}
    for k, v in db.get("mood_logs", {}).items():
        try:
            d = datetime.fromisoformat(k).date()
        except Exception:
            try:
                d = date.fromisoformat(k)
            except Exception:
                d = datetime.now().date()
        mood_logs[d] = v
    db["mood_logs"] = mood_logs

    db.setdefault("user", {"id": "alex", "name": "Alex", "goal": "",
                  "known_trigger": ""})
    return db


def _serialize_db(db: dict) -> dict:
    out = {}
    out["user"] = db.get("user", {})

    txs = {}
    for k, v in db.get("transactions", {}).items():
        tx = v.copy()
        ts = tx.get("timestamp")
        if isinstance(ts, (datetime,)):
            tx["timestamp"] = ts.isoformat()
        else:
            tx["timestamp"] = str(ts)
        txs[k] = tx
    out["transactions"] = txs

    mood_logs = {}
    for k, v in db.get("mood_logs", {}).items():
        if isinstance(k, date):
            key = k.isoformat()
        else:
            key = str(k)
        mood_logs[key] = v
    out["mood_logs"] = mood_logs


    return out


def load_db() -> dict:
    if DB_PATH.exists():
        try:
            raw = json.loads(DB_PATH.read_text())
            return _deserialize_db(raw)
        except Exception as e:
            print(
                f"Failed to load mock DB ({DB_PATH}): {e}. Falling back to default.")

    return _deserialize_db({
        "user": {
            "id": "alex",
            "name": "Alex",
            "goal": "Save $500/month",
            "known_trigger": "",
        },
        "transactions": {},
        "mood_logs": {},
    })


def save_db(db: dict):
    try:
        serializable = _serialize_db(db)
        tmp = DB_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(serializable, indent=2))
        tmp.replace(DB_PATH)
    except Exception as e:
        print(f"Failed to save DB to {DB_PATH}: {e}")


db = load_db()


class GraphState(TypedDict):
    transaction_id: str
    user_reason: str
    context: dict
    analysis: dict


def get_context_from_db(transaction_id: str, user_reason: str) -> dict:
    print("--- TOOL: Fetching Context ---")
    tx = db["transactions"][transaction_id]
    mood_log = db["mood_logs"].get(tx["timestamp"].date())
    user = db["user"]
    return {
        "transaction": tx,
        "mood_log": mood_log,
        "user_profile": user,
        "user_reason": user_reason,
    }


def update_memory_in_db(summary: str):
    print(f"--- TOOL: Updating Memory with: '{summary}' ---")
    db["user"]["memory"].append(summary)
    if "success" in summary.lower():
        db["user"]["avoided_spending"] += 120.00
    save_db(db)


def triage_agent(state: GraphState) -> GraphState:
    print("--- NODE: Triage Agent ---")
    context = get_context_from_db(
        state["transaction_id"], state["user_reason"])
    state["context"] = context
    tx = context["transaction"]
    mood = context["mood_log"]
    if tx["timestamp"].hour >= 22 and tx["amount"] > 100 and mood and mood["rating"] <= 2:
        state["context"]["requires_deep_analysis"] = True
    else:
        state["context"]["requires_deep_analysis"] = False
    return state


def analysis_agent(state: GraphState) -> GraphState:
    print("--- NODE: Analysis Agent ---")
    state["analysis"] = {
        "motivation": "Emotional (Stress)",
        "pattern_match": "Matches user's known trigger: 'Bad work days lead to online shopping'.",
    }
    return state





def should_analyze(state: GraphState) -> str:
    print("--- ROUTER: Should Analyze? ---")
    if state["context"].get("requires_deep_analysis", False):
        print("DECISION: Yes, analyze deeply.")
        return "analyze"
    else:
        print("DECISION: No, it's a routine purchase.")
        return "end"


def _detect_mood_from_text(text: str) -> Tuple[str, int]:
    t = text.lower()
    if any(w in t for w in ["sad", "depressed", "tear", "unhappy", "down"]):
        return "sad", 1
    if any(w in t for w in ["angry", "mad", "furious", "annoyed"]):
        return "angry", 1
    if any(w in t for w in ["happy", "good", "great", "joy", "glad"]):
        return "happy", 5
    if any(w in t for w in ["okay", "fine", "meh", "so-so", "neutral"]):
        return "neutral", 3
    return "neutral", 3


workflow = StateGraph(GraphState)
workflow.add_node("triage", triage_agent)
workflow.add_node("analyze", analysis_agent)
workflow.set_entry_point("triage")
workflow.add_conditional_edges("triage", should_analyze, {
                               "analyze": "analyze", "end": END})
workflow.add_edge("analyze", END)
app_graph = workflow.compile()


def fetch_nessie_purchases(account_id: str) -> list:
    url = f"{NESSIE_BASE_URL}/accounts/{account_id}/purchases?key={NESSIE_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Nessie API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Failed to fetch from Nessie: {e}")
        return []


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/log")
def log_entry(payload: LogPayload):
    analysis = analyze_entry_with_gemini(payload.text)

    ts = datetime.fromisoformat(
        payload.timestamp) if payload.timestamp else datetime.now()

    db["mood_logs"][ts.date()] = {
        "rating": analysis["mood_rating"], "note": payload.text}
    save_db(db)

    final_amount = payload.amount if payload.amount is not None else analysis.get(
        "calculated_amount")

    created_tx = None
    if final_amount is not None and final_amount > 0:
        tx_id = f"tx_{uuid.uuid4().hex[:8]}"
        
        tx = {
            "id": tx_id,
            "merchant": analysis.get("item") or "manual-entry",
            "amount": final_amount,
            "timestamp": ts,
            "status": "reviewed",
            "user_reason": payload.text,
            "mood_label": analysis["mood_label"],
            "mood_rating": analysis["mood_rating"],
        }
        db["transactions"][tx_id] = tx
        save_db(db)
        created_tx = tx

    return {"mood": {"label": analysis["mood_label"], "rating": analysis["mood_rating"]}, "transaction": created_tx}


@app.post("/api/nessie/import/{account_id}")
def import_nessie_purchases(account_id: str):
    purchases = fetch_nessie_purchases(account_id)

    if not purchases:
        raise HTTPException(
            status_code=404, detail="No purchases found or API error")

    imported_count = 0
    analyzed_count = 0

    for purchase in purchases:
        tx_id = f"nessie_{purchase['_id']}"

        if tx_id in db["transactions"]:
            continue

        try:
            purchase_date = datetime.fromisoformat(purchase['purchase_date'])
        except:
            purchase_date = datetime.now()

        user_reason = f"Bought {purchase['description']} for ${purchase['amount']}"

        tx = {
            "id": tx_id,
            "merchant": purchase.get("description", "Unknown"),
            "amount": purchase.get("amount", 0),
            "timestamp": purchase_date,
            "status": "pending_review",
            "user_reason": user_reason,
            "mood_label": "Neutral",
            "mood_rating": 3,
        }

        db["transactions"][tx_id] = tx
        imported_count += 1

        tx["status"] = "reviewed"
        analyzed_count += 1

    save_db(db)

    return {
        "status": "success",
        "imported": imported_count,
        "analyzed": analyzed_count,
        "total_in_db": len(db["transactions"])
    }


@app.get("/api/calendar")
def get_calendar_summary():
    serial = _serialize_db(db)
    calendar = {}
    for date_str, mood in serial.get("mood_logs", {}).items():
        calendar[date_str] = {"mood": mood,
                              "spending": 0.0, "transactions": []}
    for tx in serial.get("transactions", {}).values():
        try:
            d = tx.get("timestamp", "").split("T")[0]
        except Exception:
            d = str(tx.get("timestamp", ""))
        if d not in calendar:
            calendar[d] = {"mood": None, "spending": 0.0, "transactions": []}
        calendar[d]["spending"] += float(tx.get("amount", 0) or 0)
        calendar[d]["transactions"].append(tx)
    return calendar


@app.post("/api/review/{transaction_id}")
def review_transaction(transaction_id: str):
    if transaction_id not in db["transactions"]:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    tx = db["transactions"][transaction_id]
    tx["status"] = "reviewed"
    save_db(db)
    return {"status": "complete", "data": "Transaction reviewed."}





@app.get("/api/dashboard")
def get_dashboard():
    return db["user"]


@app.get("/api/mockdb")
def get_mockdb():
    try:
        return _serialize_db(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to serialize DB: {e}")

# --- Pattern Summary Endpoint ---
class PatternSummaryPayload(BaseModel):
    user_id: str
    date: str  # ISO format date string

class PatternSummaryResponse(BaseModel):
    patterns: list
    summary: str

def deduplicate_patterns(patterns: list) -> list:
    seen = set()
    unique = []
    for p in patterns:
        norm = p.lower().strip()
        if norm not in seen:
            seen.add(norm)
            unique.append(p)
    return unique

@app.post("/api/patterns/summary", response_model=PatternSummaryResponse)
def patterns_summary(payload: PatternSummaryPayload):
    """
    Analyzes previous 7 days of user data, calls Gemini for pattern analysis, deduplicates, and returns summary.
    """
    try:
        target_date = datetime.fromisoformat(payload.date).date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")
    # Get previous 7 days
    days = [(target_date - timedelta(days=i)) for i in range(7)]
    entries = []
    for d in days:
        mood_log = db["mood_logs"].get(d)
        if mood_log:
            entries.append(mood_log["note"])
        # Also add purchase reasons for that day
        for tx in db["transactions"].values():
            tx_date = tx["timestamp"]
            if isinstance(tx_date, str):
                tx_date = datetime.fromisoformat(tx_date)
            if tx_date.date() == d:
                if tx.get("user_reason"):
                    entries.append(tx["user_reason"])
    if not entries:
        return PatternSummaryResponse(patterns=[], summary="No data for previous 7 days.")
    # Call Gemini for pattern analysis
    gemini_result = analyze_patterns_with_gemini(entries)
    patterns = deduplicate_patterns(gemini_result.get("patterns", []))
    summary = gemini_result.get("summary", "")
    return PatternSummaryResponse(patterns=patterns, summary=summary)