from sqlmodel import SQLModel, Field
from typing import Optional

class StockBase(SQLModel):
    ticker: str = Field(index=True)
    company_name: str
    sector: str
    idxic_classification: str
    current_price: float

class Stock(StockBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ValuationMetrics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True)
    dcf_value: float
    rim_value: float
    forward_pe: float
    ev_ebitda: float
    piotroski_f_score: int
    altman_z_score: float
