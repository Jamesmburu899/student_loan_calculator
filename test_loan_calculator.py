import pytest
from student_loan_calculator import calculate_monthly_payment, validate_inputs, calculate_amortization_schedule

# Test for calculating monthly payment
def test_calculate_monthly_payment():
    assert calculate_monthly_payment(10000, 5, 10) == pytest.approx(106.07, 0.01)
    assert calculate_monthly_payment(5000, 3, 5) == pytest.approx(89.44, 0.01)

# Test for validating inputs
def test_validate_inputs():
    assert validate_inputs(10000, 5, 10) == True
    assert validate_inputs(-10000, 5, 10) == False
    assert validate_inputs(10000, -5, 10) == False
    assert validate_inputs(10000, 5, -10) == False

# Test for amortization schedule calculation (without extra payments)
def test_calculate_amortization_schedule():
    schedule, total_interest = calculate_amortization_schedule(10000, 5, 10)
    assert len(schedule) == 120  # 10 years * 12 months
    assert total_interest > 0

# Test for amortization schedule with extra payments
def test_calculate_amortization_schedule_with_extra_payment():
    schedule, total_interest = calculate_amortization_schedule(10000, 5, 10, extra_payment=100)
    assert len(schedule) < 120  # With extra payments, the loan should pay off earlier
    assert total_interest < 0  # Extra payments reduce the total interest paid
