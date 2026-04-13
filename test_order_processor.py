import pytest
from order_processor import calculate_shipping_cost

def test_calculate_shipping_cost_normal_weight_non_premium():
    # base(5) + 10 * 2 = 25
    assert calculate_shipping_cost(10.0, False) == 25.0

def test_calculate_shipping_cost_normal_weight_premium():
    # (base(5) + 10 * 2) * 0.9 = 22.5
    assert calculate_shipping_cost(10.0, True) == 22.5

def test_calculate_shipping_cost_zero_weight_non_premium():
    # base(5) + 0 = 5
    assert calculate_shipping_cost(0.0, False) == 5.0

def test_calculate_shipping_cost_zero_weight_premium():
    # (base(5) + 0) * 0.9 = 4.5
    assert calculate_shipping_cost(0.0, True) == 4.5

def test_calculate_shipping_cost_negative_weight():
    # (base(5) + -5 * 2) = -5 -> though logic doesn't explicitly handle negatives, 
    # it's good to know its behavior or ensure it doesn't crash.
    assert calculate_shipping_cost(-5.0, False) == -5.0
