"""
================================================================================
SpendWise - Unit Tests for Budget Monitoring & Alert Logic
File: tests/test_budget_engine.py
Assigned Module Focus: HARSH (S26CSEU1935)
================================================================================
"""

import unittest
from modules.budget_engine import (
    compute_utilization,
    calculate_remaining_budget,
    check_category_budget,
    get_budget_alerts,
    rank_spending_categories
)


class TestBudgetEngine(unittest.TestCase):

    def test_utilization_below_70_is_normal(self):
        # 69.9% -> Normal
        util, status = compute_utilization(699.0, 1000.0)
        self.assertEqual(util, 69.9)
        self.assertEqual(status, "Normal")

    def test_utilization_exactly_70_is_spending_awareness(self):
        # Exactly 70.0% -> Spending Awareness
        util, status = compute_utilization(700.0, 1000.0)
        self.assertEqual(util, 70.0)
        self.assertEqual(status, "Spending Awareness")

    def test_utilization_between_70_and_90(self):
        # 85.0% -> Spending Awareness
        util, status = compute_utilization(850.0, 1000.0)
        self.assertEqual(util, 85.0)
        self.assertEqual(status, "Spending Awareness")

    def test_utilization_exactly_90_is_high_spending_warning(self):
        # Exactly 90.0% -> High Spending Warning
        util, status = compute_utilization(900.0, 1000.0)
        self.assertEqual(util, 90.0)
        self.assertEqual(status, "High Spending Warning")

    def test_utilization_between_90_and_100(self):
        # 95.0% -> High Spending Warning
        util, status = compute_utilization(950.0, 1000.0)
        self.assertEqual(util, 95.0)
        self.assertEqual(status, "High Spending Warning")

    def test_utilization_exactly_100_is_budget_exceeded(self):
        # Exactly 100.0% -> Budget Exceeded
        util, status = compute_utilization(1000.0, 1000.0)
        self.assertEqual(util, 100.0)
        self.assertEqual(status, "Budget Exceeded")

    def test_utilization_above_100_is_budget_exceeded(self):
        # 120.0% -> Budget Exceeded
        util, status = compute_utilization(1200.0, 1000.0)
        self.assertEqual(util, 120.0)
        self.assertEqual(status, "Budget Exceeded")

    def test_zero_budget_and_zero_expenses(self):
        util, status = compute_utilization(0.0, 0.0)
        self.assertEqual(util, 0.0)
        self.assertEqual(status, "Unbudgeted")

    def test_zero_budget_and_positive_expenses_unbudgeted_spend(self):
        # Budget is 0, but spent 500 -> Must NOT divide by zero or mark as exceeded!
        util, status = compute_utilization(500.0, 0.0)
        self.assertIsNone(util)
        self.assertEqual(status, "Unbudgeted Spend")

    def test_calculate_remaining_budget(self):
        self.assertEqual(calculate_remaining_budget(5000.0, 3200.0), 1800.0)
        # Overspent by 500
        self.assertEqual(calculate_remaining_budget(5000.0, 5500.0), -500.0)

    def test_check_category_budget_details(self):
        audit = check_category_budget("Food", 4500.0, 5000.0)
        self.assertEqual(audit["category"], "Food")
        self.assertEqual(audit["spent"], 4500.0)
        self.assertEqual(audit["budget"], 5000.0)
        self.assertEqual(audit["remaining"], 500.0)
        self.assertEqual(audit["utilization_pct"], 90.0)
        self.assertEqual(audit["status"], "High Spending Warning")
        self.assertEqual(audit["status_code"], "warning")

    def test_get_budget_alerts_prioritization(self):
        cat_budgets = {"Food": 5000.0, "Shopping": 3000.0, "Bills": 2000.0}
        cat_expenses = {"Food": 4600.0, "Shopping": 3500.0, "Bills": 1500.0}
        total_budget = 10000.0
        total_expenses = 9600.0  # 96% -> Overall High Spending Warning

        alerts = get_budget_alerts(cat_budgets, cat_expenses, total_budget, total_expenses)
        self.assertTrue(len(alerts) >= 2)

        # Check Shopping exceeded alert exists
        shopping_alerts = [a for a in alerts if a["category"] == "Shopping"]
        self.assertEqual(len(shopping_alerts), 1)
        self.assertEqual(shopping_alerts[0]["severity"], "CRITICAL")
        self.assertEqual(shopping_alerts[0]["status"], "Budget Exceeded")

        # Check Food warning alert exists (92% utilization)
        food_alerts = [a for a in alerts if a["category"] == "Food"]
        self.assertEqual(len(food_alerts), 1)
        self.assertEqual(food_alerts[0]["status"], "High Spending Warning")

    def test_rank_spending_categories(self):
        cat_expenses = {
            "Food": 4000.0,
            "Transport": 1200.0,
            "Shopping": 6500.0,
            "Entertainment": 500.0
        }
        cat_budgets = {
            "Food": 5000.0,
            "Transport": 2000.0,
            "Shopping": 5000.0,
            "Entertainment": 1000.0
        }
        ranked = rank_spending_categories(cat_expenses, cat_budgets)

        self.assertEqual(ranked[0]["category"], "Shopping")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[0]["spent"], 6500.0)
        self.assertEqual(ranked[0]["status"], "Budget Exceeded")

        self.assertEqual(ranked[1]["category"], "Food")
        self.assertEqual(ranked[1]["rank"], 2)


if __name__ == "__main__":
    unittest.main()
