from typing import Dict, List


class FinancialAdvisorAgent:

    def generate_insight(
        self,
        portfolio: Dict,
        market_sentiment: str,
        sector_trends: Dict,
        news: List[Dict],
    ) -> Dict:

        holdings = portfolio.get("holdings", [])


        contributions = []

        for h in holdings:
            weight = h.get("weight_in_portfolio", 0)
            change = h.get("day_change_percent", 0)

            impact = weight * change / 100
            contributions.append({
                "symbol": h["symbol"],
                "sector": h.get("sector"),
                "impact": impact,
                "weight": weight
            })

        # Sort by impact
        contributions.sort(key=lambda x: abs(x["impact"]), reverse=True)

        top = contributions[:3]


        sector_weights = {}
        for h in holdings:
            sector = h.get("sector", "UNKNOWN")
            sector_weights[sector] = sector_weights.get(sector, 0) + h.get("weight_in_portfolio", 0)

        dominant_sector = max(sector_weights, key=sector_weights.get)


        relevant_news = [
            n for n in news
            if dominant_sector in n.get("entities", {}).get("sectors", [])
        ]

        # prioritize HIGH impact
        relevant_news.sort(key=lambda x: x.get("impact_level") == "HIGH", reverse=True)

        primary_news = relevant_news[0] if relevant_news else None


        conflicts = []
        for h in holdings:
            stock_news = [
                n for n in news
                if h["symbol"] in n.get("entities", {}).get("stocks", [])
            ]

            for n in stock_news:
                if n["sentiment"] == "POSITIVE" and h["day_change_percent"] < 0:
                    conflicts.append(f"{h['symbol']} fell despite positive news")


        explanation = f"""
Market Sentiment: {market_sentiment}

Your portfolio declined primarily due to the {dominant_sector} sector ({sector_trends.get(dominant_sector, 0)}%).

Primary Driver:
{primary_news['headline'] if primary_news else 'No major news identified'}

Top Contributors:
"""

        for c in top:
            explanation += f"\n- {c['symbol']} ({c['weight']:.1f}% weight) contributed {c['impact']:.2f}%"

        explanation += f"""

Causal Chain:
Macro News → {dominant_sector} Sector → Key Holdings → Portfolio Impact
"""

        if conflicts:
            explanation += "\n\n Conflicting Signals:"
            for c in conflicts[:2]:
                explanation += f"\n- {c}"


        confidence = 0.6
        if primary_news:
            confidence += 0.2
        if len(conflicts) == 0:
            confidence += 0.1

        return {
            "explanation": explanation.strip(),
            "confidence": round(confidence, 2)
        }