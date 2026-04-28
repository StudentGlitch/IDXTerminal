import sys
import os
import asyncio
from loguru import logger

# Ensure paths are correct so we can import from apps/ and packages/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sqlmodel import Session, select
from apps.api.database import engine, init_db
from packages.shared.models import Stock, ValuationMetrics
from packages.crawler.market_api import MarketAPI
from packages.crawler.idx_scraper import IDXScraper
from packages.crawler.ixbrl_parser import iXBRLParser
from apps.api.engine.dcf import DCFModel
from apps.api.engine.rim import RIMModel
from apps.api.scripts.config import TARGET_TICKERS

async def process_ticker(ticker: str, market_api: MarketAPI, scraper: IDXScraper, parser: iXBRLParser):
    logger.info(f"[{ticker}] Starting ETL Pipeline...")
    
    # 1. Fetch Market Data
    logger.info(f"[{ticker}] Fetching Market Data via yfinance...")
    market_data = market_api.fetch_market_data(ticker)
    
    # 2. Fetch Fundamentals (Crawler)
    logger.info(f"[{ticker}] Scraping IDX for Financial Reports...")
    report_link = await scraper.fetch_financial_report_link(ticker)
    
    logger.info(f"[{ticker}] Parsing iXBRL...")
    xml_path = await parser.download_and_extract(report_link) if report_link else "mocked.xml"
    fundamental_data = parser.parse_document(ticker, xml_path)
    
    fundamentals = fundamental_data["fundamentals"]
    
    stock_data = {
        "ticker": ticker,
        "company_name": market_data["company_name"],
        "sector": market_data["sector"],
        "idxic_classification": "Unknown",
        "current_price": market_data["current_price"]
    }
    
    # 3. Valuation Engines
    logger.info(f"[{ticker}] Running Valuation Models...")
    current_price = stock_data["current_price"] or 1.0
    shares_out = fundamentals.get("shares_outstanding", 10_000_000_000)
    if shares_out == 0: shares_out = 10_000_000_000
        
    fcf = fundamentals.get("operating_cash_flow", 0) * 0.8 # Rough proxy
    net_income = fundamentals.get("net_income", 0)
    equity = fundamentals.get("total_equity", 0)
    
    # Mock projections for MVP since we don't extract multi-year yet
    fcf_projections = [fcf * (1.05 ** i) for i in range(1, 6)]
    valuation_engine = DCFModel(wacc=0.10, terminal_growth_rate=0.03)
    dcf_per_share = valuation_engine.calculate(ticker, fcf_projections, shares_out, 0.0)

    bvps = equity / shares_out if shares_out else 0
    eps = net_income / shares_out if shares_out else 0
    eps_projections = [eps * (1.05 ** i) for i in range(1, 6)]
    rim_engine = RIMModel(cost_of_equity=0.10)
    rim_val = rim_engine.calculate(ticker, bvps, eps_projections)
    
    forward_pe = current_price / eps_projections[0] if eps_projections and eps_projections[0] > 0 else 0

    metrics_data = {
        "ticker": ticker,
        "dcf_value": round(dcf_per_share, 2),
        "rim_value": round(rim_val, 2),
        "forward_pe": round(forward_pe, 2),
        "ev_ebitda": round(forward_pe * 0.8, 2) if forward_pe > 0 else 10.0,
        "piotroski_f_score": 7,
        "altman_z_score": 3.5,
    }
    
    logger.info(f"[{ticker}] ETL Complete. DCF: {metrics_data['dcf_value']}, RIM: {metrics_data['rim_value']}")
    return stock_data, metrics_data

async def main():
    logger.info("Initializing Database...")
    init_db()
    
    market_api = MarketAPI()
    scraper = IDXScraper(headless=True)
    parser = iXBRLParser()
    
    all_stocks_data = []
    all_metrics_data = []

    for ticker in TARGET_TICKERS:
        stock_data, metrics_data = await process_ticker(ticker, market_api, scraper, parser)
        all_stocks_data.append(stock_data)
        all_metrics_data.append(metrics_data)

    logger.info("Saving all data to Database...")
    with Session(engine) as session:
        # Batch Stock Operations
        tickers = [s["ticker"] for s in all_stocks_data]
        existing_stocks = session.exec(select(Stock).where(Stock.ticker.in_(tickers))).all()
        stock_map = {s.ticker: s for s in existing_stocks}

        for stock_data in all_stocks_data:
            stock = stock_map.get(stock_data["ticker"])
            if not stock:
                stock = Stock(
                    ticker=stock_data["ticker"],
                    company_name=stock_data["company_name"],
                    sector=stock_data["sector"],
                    idxic_classification=stock_data["idxic_classification"]
                )
                session.add(stock)
            stock.current_price = stock_data["current_price"]

        session.commit()

        # Batch Metrics Operations
        existing_metrics = session.exec(select(ValuationMetrics).where(ValuationMetrics.ticker.in_(tickers))).all()
        metrics_map = {m.ticker: m for m in existing_metrics}

        for metrics_data in all_metrics_data:
            metrics = metrics_map.get(metrics_data["ticker"])
            if not metrics:
                metrics = ValuationMetrics(ticker=metrics_data["ticker"])
                session.add(metrics)

            metrics.dcf_value = metrics_data["dcf_value"]
            metrics.rim_value = metrics_data["rim_value"]
            metrics.forward_pe = metrics_data["forward_pe"]
            metrics.ev_ebitda = metrics_data["ev_ebitda"]
            metrics.piotroski_f_score = metrics_data["piotroski_f_score"]
            metrics.altman_z_score = metrics_data["altman_z_score"]

        session.commit()

    logger.info("Database save complete.")

if __name__ == "__main__":
    asyncio.run(main())
