class DCFModel:
    def __init__(self, wacc: float = 0.10, terminal_growth_rate: float = 0.02):
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate

    def calculate(self, ticker: str, fcf_projections: list, shares_outstanding: int, net_debt: float):
        """
        Calculate DCF value per share.
        
        :param ticker: Stock ticker
        :param fcf_projections: List of projected Free Cash Flows for the next N years
        :param shares_outstanding: Total number of shares outstanding
        :param net_debt: Total debt minus cash and cash equivalents
        :return: Implied share price
        """
        if not fcf_projections or shares_outstanding <= 0:
            return 0.0

        # Calculate Present Value of Free Cash Flows
        pv_fcf = 0
        for i, fcf in enumerate(fcf_projections, start=1):
            pv_fcf += fcf / ((1 + self.wacc) ** i)
        
        # Calculate Terminal Value
        # TV = FCF_n * (1 + g) / (WACC - g)
        last_fcf = fcf_projections[-1]
        terminal_value = last_fcf * (1 + self.terminal_growth_rate) / (self.wacc - self.terminal_growth_rate)
        
        # Present Value of Terminal Value
        pv_tv = terminal_value / ((1 + self.wacc) ** len(fcf_projections))
        
        # Enterprise Value
        enterprise_value = pv_fcf + pv_tv
        
        # Equity Value = Enterprise Value - Net Debt
        equity_value = enterprise_value - net_debt
        
        # Value per Share
        value_per_share = equity_value / shares_outstanding
        
        return max(0.0, value_per_share)

