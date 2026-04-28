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

async def process_ticker(ticker: str, session: Session, market_api: MarketAPI, scraper: IDXScraper, parser: iXBRLParser):
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
    
    # Check if stock exists
    stock = session.exec(select(Stock).where(Stock.ticker == ticker)).first()
    if not stock:
        stock = Stock(
            ticker=ticker,
            company_name=market_data["company_name"],
            sector=market_data["sector"],
            idxic_classification="Unknown"
        )
    
    stock.current_price = market_data["current_price"]
    
    session.add(stock)
    session.commit()
    session.refresh(stock)
    
    # 3. Valuation Engines
    logger.info(f"[{ticker}] Running Valuation Models...")
    current_price = stock.current_price or 1.0
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

    metrics = session.exec(select(ValuationMetrics).where(ValuationMetrics.ticker == ticker)).first()
    if not metrics:
        metrics = ValuationMetrics(ticker=ticker)
        
    metrics.dcf_value = round(dcf_per_share, 2)
    metrics.rim_value = round(rim_val, 2)
    metrics.forward_pe = round(forward_pe, 2)
    # Using simple heuristic or default values for uncalculated fields
    metrics.ev_ebitda = round(forward_pe * 0.8, 2) if forward_pe > 0 else 10.0
    metrics.piotroski_f_score = 7 
    metrics.altman_z_score = 3.5 
    
    session.add(metrics)
    session.commit()
    logger.info(f"[{ticker}] ETL Complete. Saved to Database. DCF: {metrics.dcf_value}, RIM: {metrics.rim_value}")

async def main():
    logger.info("Initializing Database...")
    init_db()
    
    market_api = MarketAPI()
    scraper = IDXScraper(headless=True)
    parser = iXBRLParser()
    
    with Session(engine) as session:
        for ticker in TARGET_TICKERS:
            await process_ticker(ticker, session, market_api, scraper, parser)

if __name__ == "__main__":
    asyncio.run(main())
