import numpy as np

class RIMModel:
    def __init__(self, cost_of_equity: float = 0.10):
        self.cost_of_equity = cost_of_equity

    def calculate(self, ticker: str, book_value_per_share: float, eps_projections: list):
        """
        Calculate Residual Income Model (RIM) value per share.
        
        :param ticker: Stock ticker
        :param book_value_per_share: Current Book Value Per Share (BVPS)
        :param eps_projections: List of projected Earnings Per Share for the next N years
        :return: Implied share price
        """
        if not eps_projections or book_value_per_share <= 0:
            return 0.0

        intrinsic_value = book_value_per_share
        current_bvps = book_value_per_share

        for i, eps in enumerate(eps_projections, start=1):
            # Residual Income = EPS - (Cost of Equity * Beginning BVPS)
            residual_income = eps - (self.cost_of_equity * current_bvps)
            
            # Present Value of Residual Income
            pv_ri = residual_income / ((1 + self.cost_of_equity) ** i)
            
            intrinsic_value += pv_ri
            
            # Update BVPS for next year (assuming all earnings are retained for simplicity)
            current_bvps += eps

        return max(0.0, intrinsic_value)

