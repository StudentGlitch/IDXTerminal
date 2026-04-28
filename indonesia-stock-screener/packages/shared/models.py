from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class StockBase(SQLModel):
    ticker: str = Field(index=True)
    company_name: str
    sector: str
    idxic_classification: str
    current_price: float

    @field_validator('current_price')
    def current_price_non_negative(cls, v):
        if v < 0:
            raise ValueError('current_price must be non-negative')
        return v

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
