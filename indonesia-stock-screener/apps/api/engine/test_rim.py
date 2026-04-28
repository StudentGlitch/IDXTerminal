import pytest
from apps.api.engine.rim import RIMModel

def test_calculate_no_projections():
    model = RIMModel()
    assert model.calculate("AAPL", 10.0, []) == 0.0
    # Ignoring type checker for the edge case intentionally
    assert model.calculate("AAPL", 10.0, None) == 0.0  # type: ignore

def test_calculate_negative_or_zero_bvps():
    model = RIMModel()
    assert model.calculate("AAPL", 0.0, [1.0]) == 0.0
    assert model.calculate("AAPL", -5.0, [1.0]) == 0.0

def test_calculate_positive_residual_income():
    model = RIMModel(cost_of_equity=0.10)
    result = model.calculate("AAPL", 10.0, [2.0, 2.5])
    # Expected manual calculation:
    # Year 1: RI = 2.0 - (0.10 * 10) = 1.0
    # PV RI 1 = 1.0 / 1.1 = 0.9090909090909091
    # BVPS = 10 + 2 = 12
    # Year 2: RI = 2.5 - (0.10 * 12) = 1.3
    # PV RI 2 = 1.3 / 1.21 = 1.0743801652892562
    # Intrinsic Value = 10 + 0.9090909090909091 + 1.0743801652892562 = 11.983471074380166
    assert result == pytest.approx(11.983471074380166)

def test_calculate_negative_intrinsic_value():
    model = RIMModel(cost_of_equity=0.10)
    # BVPS is low, EPS projections are highly negative causing intrinsic value to drop below 0
    result = model.calculate("AAPL", 1.0, [-5.0])
    assert result == 0.0
