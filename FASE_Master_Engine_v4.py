# --- HEALY VECTOR LABS | FASE x VERITAS v4.1 ---
# PRODUCTION STATUS: STABLE | 2026-04-14 DEPLOYMENT
import yfinance as yf
from GoogleNews import GoogleNews
import math
import time
from textblob import TextBlob
from datetime import datetime

def apply_feds_decay(initial_signal, timestamp):
    """FEDS Engine: Entropy decay via e^(-2t)"""
    now = time.time()
    t = (now - timestamp) / 86400  # Delta in days
    return initial_signal * math.exp(-2 * t)

class FASE_Engine:
    def __init__(self, ticker):
        self.ticker = ticker
        self.gn = GoogleNews(period='1d', lang='en')
        self.energy_anchor = "XLE" 

    def get_agentic_sentiment(self):
        """Scrapes multiple search vectors to ensure the net is wide."""
        queries = [f"{self.ticker} stock news", f"{self.ticker} AI data center", f"{self.ticker} playoff probability"]
        all_headlines = []
        for q in queries:
            self.gn.clear()
            self.gn.search(q)
            results = self.gn.result()
            if results:
                all_headlines.extend([res.get('title', '') for res in results if res and res.get('title')])

        if not all_headlines: 
            return 0.5
            
        # FEDS Logic: Apply e^(-2t) decay to news signals
        scores = [apply_feds_decay(TextBlob(h).sentiment.polarity, time.time()) for h in all_headlines]
        return round((sum(scores)/len(scores) + 1) / 2, 2)

    def get_variable_8_tax(self):
        """VARIABLE 8: The 'Power Tax' Audit."""
        energy_data = yf.Ticker(self.energy_anchor).history(period='5d')
        current_xle = energy_data['Close'].iloc[-1]
        energy_avg = energy_data['Close'].mean()
        tax = 0.0
        if current_xle > energy_avg:
            tax = 0.15 
        return tax

    def veritas_handshake(self, sentiment_score, hormuz_factor, energy_tax):
        """The Multi-Variable Truth Audit."""
        truth_base = sentiment_score * hormuz_factor
        return round(truth_base - energy_tax, 2)

if __name__ == "__main__":
    target_ticker = input("ENTER TICKER OR TARGET: ").upper()
    try:
        fase = FASE_Engine(target_ticker)
        sentiment = fase.get_agentic_sentiment()
        hormuz_multiplier = 0.11
        energy_tax = fase.get_variable_8_tax()
        final_truth = fase.veritas_handshake(sentiment, hormuz_multiplier, energy_tax)
        
        print("\n--- KINETIC ALPHA AUDIT ---")
        print(f"Target: {target_ticker}")
        print(f"Agentic Sentiment: {sentiment}")
        print(f"Variable 8 Tax: {energy_tax}")
        print(f"VERITAS Ground Truth: {final_truth}")
        print("---------------------------\n")
    except Exception as e:
        print(f"ENGINE FAULT: {e}")

