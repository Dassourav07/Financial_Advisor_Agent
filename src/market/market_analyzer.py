from typing import Dict, List, Union, Any


class MarketAnalyzer:

    def get_market_sentiment(self, indices: Dict[str, Any]) -> str:

        nifty_data = indices.get("NIFTY50", {})
        nifty_change = nifty_data.get("change_percent", 0)

        if nifty_change <= -0.5:
            return "BEARISH"
        elif nifty_change >= 0.5:
            return "BULLISH"
        return "NEUTRAL"


    def sector_trends(self, stocks: Union[Dict[str, Dict], List[Dict]]) -> Dict[str, float]:

        sector_perf: Dict[str, List[float]] = {}


        if isinstance(stocks, dict):
            iterable = stocks.values()


        elif isinstance(stocks, list):
            iterable = stocks

        else:
            return {}

        for stock in iterable:
            if not isinstance(stock, dict):
                continue

            sector = stock.get("sector")
            change = stock.get("change_percent")

            if sector is None or change is None:
                continue

            sector_perf.setdefault(sector, []).append(float(change))

        # Compute averages
        return {
            sector: round(sum(values) / len(values), 2)
            for sector, values in sector_perf.items()
            if values
        }

    def classify_news(self, news: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:


        categorized = {
            "market": [],
            "sector": [],
            "stock": []
        }

        for article in news:
            scope = article.get("scope", "").upper()

            if scope == "MARKET_WIDE":
                categorized["market"].append(article)

            elif scope == "SECTOR_SPECIFIC":
                categorized["sector"].append(article)

            elif scope == "STOCK_SPECIFIC":
                categorized["stock"].append(article)

            else:
                # fallback: treat unknown as market-level
                categorized["market"].append(article)

        return categorized


    def summarize_news_sentiment(self, news: List[Dict[str, Any]]) -> Dict[str, float]:
        summary = {
            "market": [],
            "sector": [],
            "stock": []
        }

        classified = self.classify_news(news)

        for key in summary:
            scores = [
                article.get("sentiment_score", 0)
                for article in classified[key]
                if isinstance(article.get("sentiment_score"), (int, float))
            ]

            if scores:
                summary[key] = round(sum(scores) / len(scores), 2)
            else:
                summary[key] = 0.0

        return summary