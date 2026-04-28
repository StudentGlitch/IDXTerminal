class MultiplesModel:

    def calculate(self, ticker: str, current_price: float, eps: float, ebitda: float, ev: float, peer_avg_pe: float = 15.0, peer_avg_ev_ebitda: float = 10.0):
        """
        Calculate valuation multiples and implied prices based on peers.
        """
        forward_pe = current_price / eps if eps > 0 else None
        ev_ebitda = ev / ebitda if ebitda > 0 else None
        
        implied_price_pe = eps * peer_avg_pe if eps > 0 else 0.0
        # Implied EV from EBITDA multiple
        implied_ev = ebitda * peer_avg_ev_ebitda if ebitda > 0 else 0.0
        
        return {
            "forward_pe": forward_pe,
            "ev_ebitda": ev_ebitda,
            "implied_price_from_pe": implied_price_pe,
            "implied_ev_from_ebitda": implied_ev
        }

