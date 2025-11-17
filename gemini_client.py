import google.generativeai as genai
import os
import time
import random
import threading
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Stable, high-limit model for PoC
model = genai.GenerativeModel("gemini-2.5-flash")


# =======================================================
# ADVANCED CIRCUIT BREAKER + BACKOFF CONFIG
# =======================================================
MAX_REQUESTS_PER_MIN = 8        # safer than free-tier limit (10)
COOLDOWN_SECONDS = 60           # if tripped, wait 1 minute
MAX_RETRIES = 5                 # attempt up to 5 retries
INITIAL_BACKOFF = 2             # first retry = 2 seconds
BACKOFF_MULTIPLIER = 2          # exponential: 2 → 4 → 8 → 16...
MAX_BACKOFF = 20                # cap wait
JITTER = True                   # add randomness to avoid spikes


# Shared global state
request_count = 0
circuit_open = False
lock = threading.Lock()


# =======================================================
# INTERNAL UTILITY
# =======================================================

def _reset_request_count():
    """Auto-reset the request counter every minute."""
    global request_count
    while True:
        time.sleep(60)
        request_count = 0

# Run counter resetter in background:
threading.Thread(target=_reset_request_count, daemon=True).start()



def _should_trip_circuit():
    """If too many requests, trip the circuit breaker."""
    global circuit_open, request_count

    with lock:
        if request_count >= MAX_REQUESTS_PER_MIN:
            circuit_open = True
            print(f"⚠️ Rate limit threshold hit. Circuit OPEN for {COOLDOWN_SECONDS}s.")
            return True
        return False



def _start_circuit_cooldown():
    """Close circuit after cooldown period."""
    global circuit_open
    time.sleep(COOLDOWN_SECONDS)
    print("🔄 Circuit CLOSED. Resuming requests.")
    circuit_open = False



# =======================================================
# ADVANCED GEMINI CALL
# =======================================================

def ask_gemini(prompt: str):
    """
    Advanced Gemini call with:
    - Circuit breaker
    - Exponential backoff
    - Google-reported retry delays
    - Jitter
    - Thread-safe request tracking
    """

    global request_count, circuit_open

    # ========== Circuit breaker check ==========
    if circuit_open:
        return "⛔ The AI is cooling down due to rate limits. Try again in 1 minute."

    # Count request attempt
    with lock:
        request_count += 1

    if _should_trip_circuit():
        # Fire cooldown in background
        threading.Thread(target=_start_circuit_cooldown, daemon=True).start()
        return "⛔ Too many requests — system is cooling down. Try again shortly."

    # ========== Retry loop ==========
    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            return response.text

        except ResourceExhausted as e:
            # Google's own recommended retry time
            retry_delay = getattr(e, "retry_delay", None)

            if retry_delay:
                print(f"⚠️ Google says retry in {retry_delay}s. Waiting...")
                time.sleep(retry_delay)
            else:
                # Exponential backoff with jitter
                wait = min(backoff, MAX_BACKOFF)
                if JITTER:
                    wait = wait + random.uniform(0, 1.5)

                print(f"⚠️ Rate limit. Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
                backoff *= BACKOFF_MULTIPLIER

        except Exception as e:
            print(f"❌ Unexpected Gemini error: {e}")
            return "❌ Gemini API failed unexpectedly. Check logs."

    # If all retries fail:
    return "❌ Gemini API is overloaded. Try again later."