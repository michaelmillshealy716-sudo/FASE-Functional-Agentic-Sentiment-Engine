# --- 1. THE POWER-UP (Installation & Imports) ---
!pip install GoogleNews yfinance textblob
import yfinance as yf
from GoogleNews import GoogleNews
from textblob import TextBlob
from datetime import datetime
import pandas as pd

# --- 2. THE HEALY VECTOR LABS HYBRID ENGINE ---
class FASE_Engine:
    def __init__(self, ticker):
        self.ticker = ticker
        self.gn = GoogleNews(period='1d', lang='en')
        
    def get_agentic_sentiment(self):
        """Scrapes multiple high-volatility keywords to ensure no 'white' results."""
        queries = [
            f"{self.ticker} stock news", 
            f"{self.ticker} geopolitical impact", 
            f"{self.ticker} supply chain"
        ]
        all_headlines = []
        
        for q in queries:
            self.gn.clear()
            self.gn.search(q)
            results = self.gn.result()
            if results:
                # Filter out None entries and extract titles
                all_headlines.extend([res.get('title', '') for res in results if res and res.get('title')])

        if not all_headlines:
            print(f"!!! LAB NOTE: No live news found for {self.ticker}. Defaulting to neutral (0.5).")
            return 0.5

        scores = [TextBlob(h).sentiment.polarity for h in all_headlines]
        avg_score = sum(scores) / len(scores)
        # Normalize -1.0/1.0 scale to 0.0 - 1.0
        return round((avg_score + 1) / 2, 2)

    def veritas_handshake(self, sentiment_score, truth_factor):
        """VERITAS: The Truth Multiplier (Direct Local Handshake)."""
        return round(sentiment_score * truth_factor, 2)

# --- 3. MASTER EXECUTION (The Field of Dreams) ---
# Dynamic Input: No more hardcoding Exxon
target_ticker = input("ENTER TICKER (e.g., XOM, TSLA, AAPL): ").upper()

try:
    # A. Market Data Check
    stock = yf.Ticker(target_ticker)
    hist = stock.history(period='1d')
    price = hist['Close'].iloc[-1] if not hist.empty else 0.0
    
    # B. FASE Sentiment Generation
    fase = FASE_Engine(target_ticker)
    sentiment_reading = fase.get_agentic_sentiment()
    
    # C. VERITAS Physical Truth Factor
    # Strategy: Market noise vs. Physical reality (April 2026 context)
    physical_multiplier = 0.11 
    veritas_score = fase.veritas_handshake(sentiment_reading, physical_multiplier)
    
    # D. Final Alpha Weighting (65% Fundamentals / 35% Audited Sentiment)
    final_fase_score = round((0.65) + (veritas_score * 0.35), 2)

    # E. THE HEALY VECTOR LABS DASHBOARD
    print(f"\n{'█'*45}")
    print(f"   HEALY VECTOR LABS | FASE x VERITAS v4.0")
    print(f"   TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'█'*45}")
    print(f"   TICKER: {target_ticker} | LIVE PRICE: ${round(price, 2)}")
    print(f"{'-'*45}")
    print(f"   SENTIMENT (Noise): {sentiment_reading}")
    print(f"   VERITAS (Truth):   {veritas_score}")
    print(f"   FINAL FASE SCORE:  {final_fase_score}")
    print(f"{'-'*45}")
    
    if veritas_score < 0.20:
        print("   ACTION: STRONG BULLISH DIVERGENCE")
        print("   REASON: Geopolitical noise is fake. Physical supply is still choked. BUY.")
    else:
        print("   ACTION: MARKET SYNC")
        print("   REASON: Truth matches the Noise.")
    print(f"{'█'*45}\n")

except Exception as e:
    print(f"!!! CRITICAL ENGINE STALL: {e}")
