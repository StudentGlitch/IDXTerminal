from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.shared.models import ValuationMetrics
from database import get_session
from engine.dcf import DCFModel
from engine.rim import RIMModel
from engine.multiples import MultiplesModel

router = APIRouter()

@router.get("/{ticker}")
def get_valuation(ticker: str, session: Session = Depends(get_session)):
    ticker = ticker.upper()
    valuation = session.exec(select(ValuationMetrics).where(ValuationMetrics.ticker == ticker)).first()
    
    if not valuation:
        # Mock calculating on-the-fly if missing in DB
        dcf = DCFModel().calculate(ticker, fcf_projections=[100, 110, 120, 130, 140], shares_outstanding=1000, net_debt=50)
        rim = RIMModel().calculate(ticker, book_value_per_share=50, eps_projections=[5, 6, 7])
        multiples = MultiplesModel().calculate(ticker, current_price=100, eps=5, ebitda=20, ev=150)
        
        return {
            "ticker": ticker,
            "dcf_value": dcf,
            "rim_value": rim,
            "forward_pe": multiples.get("forward_pe"),
            "ev_ebitda": multiples.get("ev_ebitda"),
            "piotroski_f_score": 7,
            "altman_z_score": 2.5,
            "status": "calculated_on_the_fly"
        }

    return valuation
