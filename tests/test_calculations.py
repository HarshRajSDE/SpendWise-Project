"""
================================================================================
SpendWise - Unit Tests for Financial Calculations
File: tests/test_calculations.py
================================================================================
"""

import unittest
from modules.calc_engine import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_net_balance,
    calculate_savings_rate,
    format_inr,
    calculate_category_expenses
)


class TestFinancialCalculations(unittest.TestCase):

    def setUp(self):
        self.sample_txns = [
            {"id": "1", "date": "2026-11-01", "type": "Income", "category": "Salary", "amount": 50000.0, "payment_mode": "Bank", "description": "Salary"},
            {"id": "2", "date": "2026-11-05", "type": "Income", "category": "Freelance", "amount": 10000.0, "payment_mode": "UPI", "description": "Gig"},
            {"id": "3", "date": "2026-11-06", "type": "Expense", "category": "Food", "amount": 3500.0, "payment_mode": "UPI", "description": "Groceries"},
            {"id": "4", "date": "2026-11-08", "type": "Expense", "category": "Transport", "amount": 1500.0, "payment_mode": "Card", "description": "Metro"},
            {"id": "5", "date": "2026-11-10", "type": "Expense", "category": "Food", "amount": 500.0, "payment_mode": "Cash", "description": "Snacks"}
        ]

    def test_total_income(self):
        total_inc = calculate_total_income(self.sample_txns)
        self.assertEqual(total_inc, 60000.0)

    def test_total_expenses(self):
        total_exp = calculate_total_expenses(self.sample_txns)
        self.assertEqual(total_exp, 5500.0)

    def test_net_balance(self):
        balance = calculate_net_balance(60000.0, 5500.0)
        self.assertEqual(balance, 54500.0)

    def test_savings_rate_normal(self):
        rate = calculate_savings_rate(10000.0, 2500.0)
        self.assertEqual(rate, 75.0)

    def test_savings_rate_zero_income(self):
        # Must return 0.0 without ZeroDivisionError
        rate = calculate_savings_rate(0.0, 5000.0)
        self.assertEqual(rate, 0.0)

    def test_savings_rate_negative_balance(self):
        # Spent 12000 on 10000 income -> -2000 balance -> -20.0% savings rate
        rate = calculate_savings_rate(10000.0, 12000.0)
        self.assertEqual(rate, -20.0)

    def test_format_inr_basic(self):
        formatted = format_inr(123456.78)
        self.assertEqual(formatted, "₹1,23,456.78")

    def test_format_inr_small_amount(self):
        formatted = format_inr(500)
        self.assertEqual(formatted, "₹500.00")

    def test_format_inr_negative(self):
        formatted = format_inr(-4500)
        self.assertEqual(formatted, "-₹4,500.00")

    def test_category_expenses_aggregation(self):
        cat_exp = calculate_category_expenses(self.sample_txns)
        self.assertEqual(cat_exp.get("Food"), 4000.0)
        self.assertEqual(cat_exp.get("Transport"), 1500.0)
        self.assertEqual(cat_exp.get("Bills"), 0.0)


if __name__ == "__main__":
    unittest.main()
