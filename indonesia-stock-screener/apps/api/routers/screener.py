from fastapi import APIRouter, Depends
from sqlmodel import Session, select
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.shared.models import Stock, ValuationMetrics
from database import get_session

router = APIRouter()

@router.get("/")
def get_screened_stocks(session: Session = Depends(get_session)):
    stocks_and_metrics = session.exec(
        select(Stock, ValuationMetrics)
        .outerjoin(ValuationMetrics, Stock.ticker == ValuationMetrics.ticker)
    ).all()
    
    # Fallback mock data if DB is empty
    if not stocks_and_metrics:
        mock_data = [
            {"ticker": "BBCA", "company_name": "Bank Central Asia Tbk", "sector": "Financials", "current_price": 9850, "margin_of_safety": 22.4, "dcf_value": 12050, "forward_pe": 24.5, "piotroski_f_score": 8, "ev_ebitda": 15.2, "altman_z_score": 4.1, "rim_value": 11500},
            {"ticker": "BBRI", "company_name": "Bank Rakyat Indonesia", "sector": "Financials", "current_price": 6200, "margin_of_safety": 31.5, "dcf_value": 8150, "forward_pe": 14.2, "piotroski_f_score": 7, "ev_ebitda": 10.1, "altman_z_score": 3.8, "rim_value": 7800},
            {"ticker": "BMRI", "company_name": "Bank Mandiri (Persero) Tbk", "sector": "Financials", "current_price": 7150, "margin_of_safety": 25.1, "dcf_value": 8950, "forward_pe": 11.8, "piotroski_f_score": 8, "ev_ebitda": 9.5, "altman_z_score": 3.9, "rim_value": 8500},
            {"ticker": "BBNI", "company_name": "Bank Negara Indonesia", "sector": "Financials", "current_price": 5900, "margin_of_safety": 42.8, "dcf_value": 8425, "forward_pe": 9.5, "piotroski_f_score": 6, "ev_ebitda": 8.2, "altman_z_score": 3.2, "rim_value": 8100},
            {"ticker": "ARTO", "company_name": "Bank Jago Tbk", "sector": "Financials", "current_price": 2850, "margin_of_safety": -15.4, "dcf_value": 2410, "forward_pe": 85.2, "piotroski_f_score": 3, "ev_ebitda": 45.1, "altman_z_score": 2.1, "rim_value": 2100},
            {"ticker": "BRIS", "company_name": "Bank Syariah Indonesia Tbk", "sector": "Financials", "current_price": 2450, "margin_of_safety": 12.5, "dcf_value": 2755, "forward_pe": 18.4, "piotroski_f_score": 7, "ev_ebitda": 12.5, "altman_z_score": 3.5, "rim_value": 2600},
        ]
        return {"data": mock_data}
        
    result = []
    for stock, metrics in stocks_and_metrics:
        item = stock.dict()
        if metrics:
            item.update(metrics.dict(exclude={"id", "ticker"}))
            # Calculate Margin of Safety
            if metrics.dcf_value and metrics.dcf_value > 0 and stock.current_price:
                item["margin_of_safety"] = round(((metrics.dcf_value - stock.current_price) / metrics.dcf_value) * 100, 2)
            else:
                item["margin_of_safety"] = 0.0
        result.append(item)
        
    return {"data": result}
