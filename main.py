from src.ingestion.data_loader import DataLoader
from src.market.market_analyzer import MarketAnalyzer
from src.portfolio.portfolio_engine import PortfolioEngine
from src.reasoning.agent import FinancialAdvisorAgent
from src.evaluation.evaluator import Evaluator
from src.observability.tracer import Tracer



def run():
    print(" Running Financial Advisor Agent...\n")


    loader = DataLoader("./data")

    market_data = loader.get_market_data()
    news = loader.get_news()
    portfolio = loader.get_portfolio("PORTFOLIO_002")

    if not portfolio:
        print(" Portfolio not found")
        return

    stocks_data = market_data.get("stocks", {})


    raw_holdings = portfolio.get("holdings", {})
    normalized_holdings = []

    if isinstance(raw_holdings, dict):

        for symbol, data in raw_holdings.items():

            # CASE 1: data is LIST 
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue

                    enriched = {
                        "symbol": symbol,
                        **item
                    }

                    if symbol in stocks_data:
                        enriched["sector"] = stocks_data[symbol].get("sector")

                    normalized_holdings.append(enriched)

            # CASE 2: data is DICT
            elif isinstance(data, dict):
                enriched = {
                    "symbol": symbol,
                    **data
                }

                if symbol in stocks_data:
                    enriched["sector"] = stocks_data[symbol].get("sector")

                normalized_holdings.append(enriched)

    elif isinstance(raw_holdings, list):

        for h in raw_holdings:
            if not isinstance(h, dict):
                continue

            symbol = h.get("symbol")

            if symbol and symbol in stocks_data:
                h["sector"] = stocks_data[symbol].get("sector")

            normalized_holdings.append(h)

    else:
        print(" Unsupported holdings format")
        return


    portfolio["holdings"] = normalized_holdings

    if not portfolio["holdings"]:
        print(" No valid holdings found")
        return


    market = MarketAnalyzer()
    portfolio_engine = PortfolioEngine()
    agent = FinancialAdvisorAgent()
    evaluator = Evaluator()


    sentiment = market.get_market_sentiment(
        market_data.get("indices", {})
    )

    sector_trends = market.sector_trends(stocks_data)


    pnl = portfolio_engine.compute_pnl(portfolio["holdings"])
    allocation = portfolio_engine.sector_allocation(portfolio["holdings"])
    risks = portfolio_engine.detect_risk(
        portfolio["holdings"],
        allocation
    )


    insight = agent.generate_insight(
        portfolio,
        sentiment,
        sector_trends,
        news
    )

    score = evaluator.score(insight["explanation"])
    
    tracer = Tracer()
    tracer.trace("agent_run", {
        "portfolio_id": "PORTFOLIO_002",
        "market_sentiment": sentiment,
        "dominant_sector": max(allocation, key=allocation.get),
        "confidence": insight["confidence"],
        "score": score
        })


    print(" Portfolio Summary")
    print(pnl)

    print("\n Sector Allocation")
    print(allocation)

    print("\n Risks")
    print(risks)

    print("\n AI Insight")
    print(insight["explanation"])

    print("\n Confidence:", insight["confidence"])
    print("Reasoning Score:", score)



if __name__ == "__main__":
    run()