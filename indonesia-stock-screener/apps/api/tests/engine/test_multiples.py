import pytest

from apps.api.engine.multiples import MultiplesModel

class TestMultiplesModel:
    def setup_method(self):
        self.model = MultiplesModel()

    def test_calculate_happy_path(self):
        """Test with normal positive values using default peers."""
        result = self.model.calculate(
            ticker="BBCA",
            current_price=10000.0,
            eps=500.0,
            ebitda=20000.0,
            ev=200000.0
        )

        assert result["forward_pe"] == 20.0
        assert result["ev_ebitda"] == 10.0
        assert result["implied_price_from_pe"] == 7500.0 # 500 * 15.0
        assert result["implied_ev_from_ebitda"] == 200000.0 # 20000 * 10.0

    def test_calculate_negative_eps(self):
        """Test with negative EPS."""
        result = self.model.calculate(
            ticker="GOTO",
            current_price=100.0,
            eps=-10.0,
            ebitda=20000.0,
            ev=200000.0
        )

        assert result["forward_pe"] is None
        assert result["implied_price_from_pe"] == 0.0
        # Other values should still calculate
        assert result["ev_ebitda"] == 10.0
        assert result["implied_ev_from_ebitda"] == 200000.0

    def test_calculate_zero_eps(self):
        """Test with zero EPS."""
        result = self.model.calculate(
            ticker="ZERO",
            current_price=100.0,
            eps=0.0,
            ebitda=20000.0,
            ev=200000.0
        )

        assert result["forward_pe"] is None
        assert result["implied_price_from_pe"] == 0.0

    def test_calculate_negative_ebitda(self):
        """Test with negative EBITDA."""
        result = self.model.calculate(
            ticker="GOTO",
            current_price=100.0,
            eps=5.0,
            ebitda=-1000.0,
            ev=200000.0
        )

        assert result["ev_ebitda"] is None
        assert result["implied_ev_from_ebitda"] == 0.0
        # Other values should still calculate
        assert result["forward_pe"] == 20.0
        assert result["implied_price_from_pe"] == 75.0

    def test_calculate_zero_ebitda(self):
        """Test with zero EBITDA."""
        result = self.model.calculate(
            ticker="ZERO",
            current_price=100.0,
            eps=5.0,
            ebitda=0.0,
            ev=200000.0
        )

        assert result["ev_ebitda"] is None
        assert result["implied_ev_from_ebitda"] == 0.0

    def test_calculate_custom_peers(self):
        """Test with custom peer averages."""
        result = self.model.calculate(
            ticker="BBCA",
            current_price=10000.0,
            eps=500.0,
            ebitda=20000.0,
            ev=200000.0,
            peer_avg_pe=25.0,
            peer_avg_ev_ebitda=15.0
        )

        assert result["forward_pe"] == 20.0
        assert result["ev_ebitda"] == 10.0
        assert result["implied_price_from_pe"] == 12500.0 # 500 * 25.0
        assert result["implied_ev_from_ebitda"] == 300000.0 # 20000 * 15.0
