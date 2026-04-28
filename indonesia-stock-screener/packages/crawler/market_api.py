import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional

class MarketAPI:
    def __init__(self):
        # We append .JK to IDX tickers for Yahoo Finance
        self.suffix = ".JK"

    def fetch_market_data(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches current price, shares outstanding, and 5-year OHLCV.
        Returns a dictionary with the necessary market data.
        """
        yf_ticker = f"{ticker}{self.suffix}"
        stock = yf.Ticker(yf_ticker)
        
        try:
            info = stock.info
            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            shares_outstanding = info.get("sharesOutstanding", 0)
            sector = info.get("sector", "Unknown")
            company_name = info.get("longName", ticker)
            
            # Fetch 5-year historical data (monthly interval is usually enough for charting MVP or daily)
            # For lightweight charts, we might want daily, but let's grab daily for 1 year or 5 years
            hist = stock.history(period="5y")
            historical_data = []
            
            if not hist.empty:
                # Reset index to get Date as a column
                hist_reset = hist.reset_index()
                hist_reset["time"] = hist_reset["Date"].dt.strftime("%Y-%m-%d")
                historical_data = hist_reset[["time", "Open", "High", "Low", "Close", "Volume"]].rename(columns={
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Volume": "volume"
                }).to_dict("records")

            return {
                "ticker": ticker,
                "company_name": company_name,
                "sector": sector,
                "current_price": current_price,
                "shares_outstanding": shares_outstanding,
                "historical_data": historical_data
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return {
                "ticker": ticker,
                "company_name": ticker,
                "sector": "Unknown",
                "current_price": 0,
                "shares_outstanding": 0,
                "historical_data": []
            }
