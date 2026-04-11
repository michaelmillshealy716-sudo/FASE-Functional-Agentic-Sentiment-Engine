# --- HEALY VECTOR LABS | FASE x VERITAS v4.1 ---
# PRODUCTION STATUS: STABLE | 2026-04-11 DEPLOYMENT
import yfinance as yf
from GoogleNews import GoogleNews
from textblob import TextBlob
from datetime import datetime

class FASE_Engine:
    def __init__(self, ticker):
        self.ticker = ticker
        self.gn = GoogleNews(period='1d', lang='en')
        self.energy_anchor = "XLE" # Variable 8: Energy Sector Proxy
        
    def get_agentic_sentiment(self):
        """Scrapes multiple search vectors to ensure the net is wide."""
        queries = [f"{self.ticker} stock news", f"{self.ticker} AI data center", f"{self.ticker} energy grid"]
        all_headlines = []
        for q in queries:
            self.gn.clear()
            self.gn.search(q)
            results = self.gn.result()
            if results:
                all_headlines.extend([res.get('title', '') for res in results if res and res.get('title')])
        
        if not all_headlines: return 0.5
        scores = [TextBlob(h).sentiment.polarity for h in all_headlines]
        return round((sum(scores)/len(scores) + 1) / 2, 2)

    def get_variable_8_tax(self):
        """VARIABLE 8: The 'Power Tax' Audit (Energy & Grid Costs)."""
        # Current Context: XLE at ~$56.94 | Louisiana 7.5GW Meta site demand
        energy_data = yf.Ticker(self.energy_anchor).history(period='5d')
        current_xle = energy_data['Close'].iloc[-1]
        energy_avg = energy_data['Close'].mean()
        
        # If Energy (XLE) is trending up, we tax the Tech 'AI Bull' logic
        tax = 0.0
        if current_xle > energy_avg:
            tax = 0.15 # 15% margin tax for data-center heavy AI compute
        return tax

    def veritas_handshake(self, sentiment_score, hormuz_factor, energy_tax):
        """The Multi-Variable Truth Audit."""
        # 0.11 Multiplier (Geopolitics) + Variable 8 (Energy Tax)
        truth_base = sentiment_score * hormuz_factor
        return round(truth_base - energy_tax, 2)

# --- MASTER EXECUTION ---
target_ticker = input("ENTER TICKER: ").upper()
try:
    fase = FASE_Engine(target_ticker)
    
    # A. Noise Level
    sentiment = fase.get_agentic_sentiment()
    
    # B. The Physical Audits (April 2026 Reality)
    hormuz_multiplier = 0.11  # Variable 5: Strait of Hormuz mine-clearing
    energy_tax = fase.get_variable_8_tax()  # Variable 8: The Energy Tax
    
    veritas_score = fase.veritas_handshake(sentiment, hormuz_multiplier, energy_tax)
    
    # C. Final Alpha Fusion (65/35 Weighted Split)
    final_alpha = round((0.65) + (veritas_score * 0.35), 2)

    print(f"\n{'█'*45}\n   HEALY VECTOR LABS | FASE x VERITAS v4.1\n{'█'*45}")
    print(f"   TICKER: {target_ticker} | LIVE SENTIMENT: {sentiment}")
    print(f"   ENERGY TAX (VAR 8): -{energy_tax}")
    print(f"   VERITAS TRUTH: {veritas_score}")
    print(f"   FINAL ALPHA SCORE: {final_alpha}")
    print(f"{'-'*45}")
    
    if veritas_score < 0.15:
        print("   STATUS: TRUTH DIVERGENCE DETECTED")
        print("   REASON: Energy costs and maritime blocks exposed market lie.")
    else:
        print("   STATUS: MARKET ALIGNMENT")
    print(f"{'█'*45}\n")

except Exception as e:
    print(f"!!! ENGINE STALL: {e}")
    
