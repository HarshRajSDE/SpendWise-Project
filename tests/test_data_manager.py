"""
================================================================================
SpendWise - Unit Tests for Data Manager Layer
File: tests/test_data_manager.py
================================================================================
"""

import unittest
import os
import shutil
import tempfile
from modules import data_manager
import config


class TestDataManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing without touching actual data
        self.test_dir = tempfile.mkdtemp()
        self.orig_transactions_file = config.TRANSACTIONS_FILE
        self.orig_budget_file = config.BUDGET_FILE
        self.orig_backups_dir = config.BACKUPS_DIR

        # Divert data paths to temp directory
        data_manager.TRANSACTIONS_FILE = os.path.join(self.test_dir, "test_transactions.csv")
        data_manager.BUDGET_FILE = os.path.join(self.test_dir, "test_budget.json")
        data_manager.BACKUPS_DIR = os.path.join(self.test_dir, "backups")

    def tearDown(self):
        # Restore original paths and remove temp directory
        data_manager.TRANSACTIONS_FILE = self.orig_transactions_file
        data_manager.BUDGET_FILE = self.orig_budget_file
        data_manager.BACKUPS_DIR = self.orig_backups_dir
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_data_files_creates_empty_files(self):
        data_manager.init_data_files()
        self.assertTrue(os.path.exists(data_manager.TRANSACTIONS_FILE))
        self.assertTrue(os.path.exists(data_manager.BUDGET_FILE))

        # Check default empty dataset
        txns = data_manager.load_transactions()
        self.assertEqual(len(txns), 0)

        budgets = data_manager.load_budget()
        self.assertEqual(budgets, {})

    def test_add_and_load_transaction(self):
        txn = {
            "date": "2026-11-15",
            "type": "Expense",
            "category": "Food",
            "amount": 750.50,
            "payment_mode": "UPI",
            "description": "Lunch"
        }
        success = data_manager.add_transaction(txn)
        self.assertTrue(success)

        loaded = data_manager.load_transactions()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["category"], "Food")
        self.assertEqual(loaded[0]["amount"], 750.50)
        self.assertTrue(len(loaded[0]["id"]) > 0)

    def test_delete_transaction(self):
        txn = {
            "id": "DEL-01",
            "date": "2026-11-15",
            "type": "Expense",
            "category": "Transport",
            "amount": 300.0,
            "payment_mode": "Cash",
            "description": "Taxi"
        }
        data_manager.add_transaction(txn)
        self.assertEqual(len(data_manager.load_transactions()), 1)

        del_success = data_manager.delete_transaction("DEL-01")
        self.assertTrue(del_success)
        self.assertEqual(len(data_manager.load_transactions()), 0)

    def test_update_transaction(self):
        txn = {
            "id": "UPD-01",
            "date": "2026-11-15",
            "type": "Expense",
            "category": "Food",
            "amount": 400.0,
            "payment_mode": "UPI",
            "description": "Lunch"
        }
        data_manager.add_transaction(txn)

        # Update amount and description
        updated_txn = {
            "id": "UPD-01",
            "date": "2026-11-15",
            "type": "Expense",
            "category": "Food",
            "amount": 550.0,
            "payment_mode": "UPI",
            "description": "Lunch with dessert"
        }
        upd_success = data_manager.update_transaction(updated_txn)
        self.assertTrue(upd_success)

        loaded = data_manager.load_transactions()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["amount"], 550.0)
        self.assertEqual(loaded[0]["description"], "Lunch with dessert")

    def test_budget_set_and_get(self):
        cat_budgets = {"Food": 5000.0, "Transport": 2000.0}
        success = data_manager.set_monthly_budget("2026-11", cat_budgets, total_budget=7000.0)
        self.assertTrue(success)

        retrieved = data_manager.get_monthly_budget("2026-11")
        self.assertEqual(retrieved["monthly_total"], 7000.0)
        self.assertEqual(retrieved["categories"]["Food"], 5000.0)
        self.assertEqual(retrieved["categories"]["Transport"], 2000.0)

    def test_invalid_transaction_amount_rejected(self):
        # Negative amount
        invalid_txn1 = {"amount": -500.0, "category": "Food", "type": "Expense"}
        self.assertFalse(data_manager.add_transaction(invalid_txn1))

        # Zero amount
        invalid_txn2 = {"amount": 0.0, "category": "Food", "type": "Expense"}
        self.assertFalse(data_manager.add_transaction(invalid_txn2))

        # Non-numeric amount
        invalid_txn3 = {"amount": "invalid_number", "category": "Food", "type": "Expense"}
        self.assertFalse(data_manager.add_transaction(invalid_txn3))

    def test_export_and_backup_operations(self):
        txn = {
            "date": "2026-11-16",
            "type": "Expense",
            "category": "Education",
            "amount": 1200.0,
            "payment_mode": "UPI",
            "description": "Textbook"
        }
        data_manager.add_transaction(txn)

        csv_content = data_manager.export_transactions_csv()
        self.assertIn("Education", csv_content)
        self.assertIn("1200.00", csv_content)

        backup_res = data_manager.backup_data()
        self.assertTrue(backup_res.get("success"))
        self.assertTrue(os.path.exists(backup_res.get("csv_backup")))

    def test_clear_all_data(self):
        data_manager.add_transaction({"amount": 100.0, "category": "Food", "type": "Expense"})
        data_manager.set_monthly_budget("2026-11", {"Food": 1000.0})
        self.assertEqual(len(data_manager.load_transactions()), 1)

        clear_res = data_manager.clear_all_data()
        self.assertTrue(clear_res)
        self.assertEqual(len(data_manager.load_transactions()), 0)
        self.assertEqual(data_manager.load_budget(), {})


if __name__ == "__main__":
    unittest.main()
