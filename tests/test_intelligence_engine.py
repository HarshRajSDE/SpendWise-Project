"""
================================================================================
SpendWise - Unit Tests for Smart Budget Intelligence Engine
File: tests/test_intelligence_engine.py
Assigned Module Focus: HARSH (S26CSEU1935)
================================================================================
"""

import unittest
from datetime import date
from modules.intelligence_engine import (
    get_month_calendar_context,
    calculate_average_daily_spending,
    calculate_monthly_forecast,
    calculate_projected_overspending,
    calculate_safe_daily_spending,
    calculate_overspending_risk_index,
    generate_budget_intelligence
)


class TestIntelligenceEngine(unittest.TestCase):

    def test_calendar_context_february_leap_year(self):
        # 2024 was a leap year: Feb has 29 days
        cal_leap = get_month_calendar_context("2024-02", as_of_date=date(2024, 2, 10))
        self.assertEqual(cal_leap["total_days"], 29)
        self.assertEqual(cal_leap["elapsed_days"], 10)
        self.assertEqual(cal_leap["remaining_days"], 20)  # 29 - 10 + 1

        # 2026 is a standard year: Feb has 28 days
        cal_non_leap = get_month_calendar_context("2026-02", as_of_date=date(2026, 2, 14))
        self.assertEqual(cal_non_leap["total_days"], 28)
        self.assertEqual(cal_non_leap["elapsed_days"], 14)
        self.assertEqual(cal_non_leap["remaining_days"], 15)  # 28 - 14 + 1

    def test_calendar_context_historical_month(self):
        # When reference is in Nov 2026, Jan 2026 is historical
        cal = get_month_calendar_context("2026-01", as_of_date=date(2026, 11, 15))
        self.assertTrue(cal["is_past"])
        self.assertFalse(cal["is_current"])
        self.assertEqual(cal["elapsed_days"], 31)
        self.assertEqual(cal["remaining_days"], 0)

    def test_average_daily_spending(self):
        # Spent 15000 in 15 days -> 1000/day
        avg = calculate_average_daily_spending(15000.0, 15)
        self.assertEqual(avg, 1000.0)

        # Zero expenses
        self.assertEqual(calculate_average_daily_spending(0.0, 15), 0.0)
        # Zero days elapsed
        self.assertEqual(calculate_average_daily_spending(5000.0, 0), 0.0)

    def test_month_end_forecast(self):
        # 1000/day across 30 days -> 30000 projected
        forecast = calculate_monthly_forecast(1000.0, 30)
        self.assertEqual(forecast, 30000.0)

    def test_projected_overspending(self):
        # Projected 35000 on 30000 budget -> Overspending = 5000
        overspend = calculate_projected_overspending(35000.0, 30000.0)
        self.assertEqual(overspend, 5000.0)

        # Projected 25000 on 30000 budget -> Overspending = 0
        overspend_safe = calculate_projected_overspending(25000.0, 30000.0)
        self.assertEqual(overspend_safe, 0.0)

    def test_safe_daily_spending_normal(self):
        # Budget = 30000, Spent = 15000, Remaining budget = 15000, 15 remaining days -> 1000/day
        safe = calculate_safe_daily_spending(30000.0, 15000.0, 15)
        self.assertEqual(safe, 1000.0)

    def test_safe_daily_spending_when_budget_exceeded(self):
        # Budget = 20000, Spent = 22000 (already exceeded) -> Safe daily spending MUST BE 0.0
        safe = calculate_safe_daily_spending(20000.0, 22000.0, 10)
        self.assertEqual(safe, 0.0)

    def test_safe_daily_spending_zero_remaining_days(self):
        # Month over (0 days left) -> 0.0
        safe = calculate_safe_daily_spending(20000.0, 10000.0, 0)
        self.assertEqual(safe, 0.0)

    def test_risk_index_low_risk_boundary(self):
        # Projected 6000 on 10000 budget -> 60% -> Score 60 (Low Risk)
        score, level, _, _ = calculate_overspending_risk_index(6000.0, 10000.0)
        self.assertEqual(score, 60)
        self.assertEqual(level, "Low Risk")

    def test_risk_index_moderate_risk_boundary(self):
        # Exactly 70% -> Score 70 (Moderate Risk)
        score_70, level_70, _, _ = calculate_overspending_risk_index(7000.0, 10000.0)
        self.assertEqual(score_70, 70)
        self.assertEqual(level_70, "Moderate Risk")

        # 89% -> Score 89 (Moderate Risk)
        score_89, level_89, _, _ = calculate_overspending_risk_index(8900.0, 10000.0)
        self.assertEqual(score_89, 89)
        self.assertEqual(level_89, "Moderate Risk")

    def test_risk_index_high_risk_boundary(self):
        # Exactly 90% -> Score 90 (High Risk)
        score_90, level_90, _, _ = calculate_overspending_risk_index(9000.0, 10000.0)
        self.assertEqual(score_90, 90)
        self.assertEqual(level_90, "High Risk")

        # 99% -> Score 99 (High Risk)
        score_99, level_99, _, _ = calculate_overspending_risk_index(9900.0, 10000.0)
        self.assertEqual(score_99, 99)
        self.assertEqual(level_99, "High Risk")

    def test_risk_index_critical_risk_boundary(self):
        # 100% -> Score 100 (Critical Risk)
        score_100, level_100, _, _ = calculate_overspending_risk_index(10000.0, 10000.0)
        self.assertEqual(score_100, 100)
        self.assertEqual(level_100, "Critical Risk")

        # Projected 15000 on 10000 budget -> clamped to 100
        score_150, level_150, _, _ = calculate_overspending_risk_index(15000.0, 10000.0)
        self.assertEqual(score_150, 100)
        self.assertEqual(level_150, "Critical Risk")

    def test_generate_budget_intelligence_full_pipeline(self):
        txns = [
            {"id": "1", "date": "2026-11-02", "type": "Income", "category": "Salary", "amount": 50000.0},
            {"id": "2", "date": "2026-11-05", "type": "Expense", "category": "Food", "amount": 3000.0},
            {"id": "3", "date": "2026-11-10", "type": "Expense", "category": "Transport", "amount": 1500.0}
        ]
        budget = {
            "monthly_total": 20000.0,
            "categories": {"Food": 6000.0, "Transport": 3000.0}
        }
        ref_date = date(2026, 11, 15)  # Nov 15: elapsed = 15 days, total = 30 days, remaining = 16 days

        intel = generate_budget_intelligence("2026-11", txns, budget, as_of_date=ref_date)

        # Income must be excluded: Total expenses = 4500.0
        self.assertEqual(intel["total_expenses"], 4500.0)
        # Average daily spending = 4500 / 15 = 300.0
        self.assertEqual(intel["avg_daily_spending"], 300.0)
        # Month forecast = 300 * 30 = 9000.0
        self.assertEqual(intel["projected_expenses"], 9000.0)
        # Projected overspending = 0 (9000 <= 20000)
        self.assertEqual(intel["projected_overspending"], 0.0)
        # Safe daily spending = (20000 - 4500) / 16 = 15500 / 16 = 968.75
        self.assertEqual(intel["safe_daily_spending"], 968.75)
        # Risk score = (9000 / 20000) * 100 = 45 -> Low Risk
        self.assertEqual(intel["risk_score"], 45)
        self.assertEqual(intel["risk_level"], "Low Risk")
        # Recommendations should be present
        self.assertTrue(len(intel["recommendations"]) > 0)


if __name__ == "__main__":
    unittest.main()
