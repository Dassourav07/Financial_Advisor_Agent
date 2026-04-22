import streamlit as st

from src.ingestion.data_loader import DataLoader
from src.market.market_analyzer import MarketAnalyzer
from src.portfolio.portfolio_engine import PortfolioEngine
from src.reasoning.agent import FinancialAdvisorAgent
from src.evaluation.evaluator import Evaluator


st.set_page_config(page_title="Financial Advisor Agent", layout="wide")

st.title(" Autonomous Financial Advisor Agent")


loader = DataLoader("./data")
market = MarketAnalyzer()
portfolio_engine = PortfolioEngine()
agent = FinancialAdvisorAgent()
evaluator = Evaluator()


portfolio_id = st.selectbox(
    "Select Portfolio",
    ["PORTFOLIO_001", "PORTFOLIO_002", "PORTFOLIO_003"]
)


if st.button("Run Analysis"):

    market_data = loader.get_market_data()
    news = loader.get_news()
    portfolio = loader.get_portfolio(portfolio_id)

    if not portfolio:
        st.error("Portfolio not found")
        st.stop()

    stocks_data = market_data.get("stocks", {})


    raw_holdings = portfolio.get("holdings", {})
    normalized_holdings = []

    if isinstance(raw_holdings, dict):
        for symbol, data in raw_holdings.items():

            if isinstance(data, list):
                for item in data:
                    enriched = {"symbol": symbol, **item}
                    if symbol in stocks_data:
                        enriched["sector"] = stocks_data[symbol].get("sector")
                    normalized_holdings.append(enriched)

            elif isinstance(data, dict):
                enriched = {"symbol": symbol, **data}
                if symbol in stocks_data:
                    enriched["sector"] = stocks_data[symbol].get("sector")
                normalized_holdings.append(enriched)

    portfolio["holdings"] = normalized_holdings


    sentiment = market.get_market_sentiment(
        market_data.get("indices", {})
    )

    sector_trends = market.sector_trends(stocks_data)

    pnl = portfolio_engine.compute_pnl(portfolio["holdings"])
    sector_alloc = portfolio_engine.sector_allocation(portfolio["holdings"])
    asset_alloc = portfolio_engine.asset_allocation(portfolio["holdings"])
    risks = portfolio_engine.detect_risk(portfolio["holdings"], sector_alloc)

    insight = agent.generate_insight(
        portfolio,
        sentiment,
        sector_trends,
        news
    )

    score = evaluator.score(insight["explanation"])


    col1, col2, col3 = st.columns(3)

    col1.metric("Portfolio Value", f"₹{pnl['total_value']}")
    col2.metric("P&L", f"₹{pnl['pnl']}")
    col3.metric("P&L %", f"{pnl['pnl_percent']}%")

    st.subheader(" Sector Allocation")
    st.bar_chart(sector_alloc)

    st.subheader(" Asset Allocation")
    st.bar_chart(asset_alloc)

    st.subheader(" Risks")
    for r in risks:
        st.warning(r)

    st.subheader("AI Insight")
    st.write(insight["explanation"])

    st.subheader("Confidence & Score")
    st.success(f"Confidence: {insight['confidence']}")
    st.info(f"Reasoning Score: {score}")
