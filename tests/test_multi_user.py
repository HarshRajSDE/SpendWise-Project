"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: tests/test_multi_user.py
Description: Automated unit test suite verifying PBKDF2 cryptography, official
             team authentication, strict multi-tenant row-level data isolation,
             and administrative access controls.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
Institution: Bennett University
================================================================================
"""

import unittest
from datetime import datetime
from modules.database import (
    hash_password,
    verify_password,
    authenticate_user,
    get_all_users,
    get_user_by_id,
    update_user_password,
    set_user_active_status,
    add_user_transaction,
    get_user_transactions,
    update_user_transaction,
    delete_user_transaction,
    set_user_monthly_budget,
    get_user_monthly_budget,
    get_audit_logs,
    init_db,
    OFFICIAL_TEAM_ROSTER
)


class TestMultiUserPlatform(unittest.TestCase):
    """
    Test suite for Multi-User authentication, PBKDF2 security, and row-level data isolation.
    """

    @classmethod
    def setUpClass(cls):
        # Ensure database is initialized with the 5 official Bennett University members
        init_db()

    def test_password_hashing_and_verification(self):
        """Verify PBKDF2-HMAC-SHA256 salted hashing and verification."""
        password = "SecurePassword123!"
        hashed = hash_password(password)

        # Hash format: salt_hex$key_hex (16-byte salt, 32-byte sha256 key)
        parts = hashed.split("$")
        self.assertEqual(len(parts), 2)
        salt_hex, key_hex = parts
        self.assertEqual(len(bytes.fromhex(salt_hex)), 16)
        self.assertEqual(len(bytes.fromhex(key_hex)), 32)

        # Correct password must verify
        self.assertTrue(verify_password(password, hashed))

        # Incorrect password must fail
        self.assertFalse(verify_password("WrongPassword!", hashed))
        self.assertFalse(verify_password("", hashed))

    def test_all_five_official_members_authenticate(self):
        """Verify all 5 official Bennett University team members can authenticate."""
        test_creds = [
            ("S26CSEU1925", "Ridhima@1925", "Ridhima", "member"),
            ("S26CSEU1922", "Anoushka@1922", "Anoushka", "member"),
            ("S26CSEU1913", "Aatirth@1913", "AATIRTH", "member"),
            ("S26CSEU1935", "Harsh@1935", "HARSH", "admin"),
            ("S26CSEU1939", "Srishthi@1939", "SRISHTHI", "member"),
        ]

        for enrollment, pin, expected_name, expected_role in test_creds:
            user = authenticate_user(enrollment, pin)
            self.assertIsNotNone(user, f"Authentication failed for {enrollment}")
            self.assertEqual(user["full_name"], expected_name)
            self.assertEqual(user["role"], expected_role)
            self.assertTrue(user["is_active"])

    def test_authentication_invalid_credentials(self):
        """Verify authentication rejects unauthorized access attempts."""
        # Invalid enrollment
        self.assertIsNone(authenticate_user("S26UNKNOWN999", "SomePassword"))
        # Valid enrollment, invalid password
        self.assertIsNone(authenticate_user("S26CSEU1935", "WrongPin@9999"))
        # Empty credentials
        self.assertIsNone(authenticate_user("", ""))

    def test_row_level_data_isolation_transactions(self):
        """
        Verify strict row-level isolation for transactions.
        Member A cannot view, update, or delete Member B's financial records.
        """
        # User 1: Ridhima (S26CSEU1925)
        # User 4: Harsh (S26CSEU1935)
        users = {u["enrollment_no"]: u for u in get_all_users()}
        ridhima = users["S26CSEU1925"]
        harsh = users["S26CSEU1935"]

        # 1. Add transaction under Ridhima's user_id
        ok_r, ridhima_txn_id = add_user_transaction(
            user_id=ridhima["id"],
            t_date="2026-11-18",
            t_type="Expense",
            category="Food & Dining",
            amount=450.0,
            payment_mode="UPI (GPay / PhonePe / Paytm)",
            description="Confidential Ridhima Lunch"
        )
        self.assertTrue(ok_r)
        self.assertIsNotNone(ridhima_txn_id)

        # 2. Add transaction under Harsh's user_id
        ok_h, harsh_txn_id = add_user_transaction(
            user_id=harsh["id"],
            t_date="2026-11-18",
            t_type="Expense",
            category="Technology & Subscriptions",
            amount=1500.0,
            payment_mode="Credit Card",
            description="Harsh Cloud Server"
        )
        self.assertTrue(ok_h)
        self.assertIsNotNone(harsh_txn_id)

        # 3. Query Ridhima's transactions - must NOT contain Harsh's transaction
        ridhima_txns = get_user_transactions(user_id=ridhima["id"])
        ridhima_descriptions = [t["description"] for t in ridhima_txns]
        self.assertIn("Confidential Ridhima Lunch", ridhima_descriptions)
        self.assertNotIn("Harsh Cloud Server", ridhima_descriptions)

        # 4. Query Harsh's transactions - must NOT contain Ridhima's transaction
        harsh_txns = get_user_transactions(user_id=harsh["id"])
        harsh_descriptions = [t["description"] for t in harsh_txns]
        self.assertIn("Harsh Cloud Server", harsh_descriptions)
        self.assertNotIn("Confidential Ridhima Lunch", harsh_descriptions)

        # 5. Security attack simulation: Harsh attempts to modify Ridhima's transaction
        success_attack, msg = update_user_transaction(
            user_id=harsh["id"],  # Unauthorized user
            txn_id=ridhima_txn_id,
            t_date="2026-11-18",
            t_type="Expense",
            category="Entertainment",
            amount=9999.0,
            payment_mode="Cash",
            description="Tampered by other user"
        )
        self.assertFalse(success_attack, "Unauthorized user was able to modify another user's transaction!")

        # Verify original record is unaltered
        ridhima_txns_after = get_user_transactions(user_id=ridhima["id"])
        target = next(t for t in ridhima_txns_after if t["id"] == ridhima_txn_id)
        self.assertEqual(target["amount"], 450.0)
        self.assertEqual(target["description"], "Confidential Ridhima Lunch")

        # 6. Security attack simulation: Harsh attempts to delete Ridhima's transaction
        attack_delete = delete_user_transaction(
            user_id=harsh["id"],  # Unauthorized user
            txn_id=ridhima_txn_id
        )
        self.assertFalse(attack_delete, "Unauthorized user was able to delete another user's transaction!")

        # 7. Authorized deletion works
        clean_delete_r = delete_user_transaction(user_id=ridhima["id"], txn_id=ridhima_txn_id)
        clean_delete_h = delete_user_transaction(user_id=harsh["id"], txn_id=harsh_txn_id)
        self.assertTrue(clean_delete_r)
        self.assertTrue(clean_delete_h)

    def test_row_level_data_isolation_budgets(self):
        """
        Verify strict budget isolation.
        Setting a budget for User A does not overwrite or expose to User B.
        """
        users = {u["enrollment_no"]: u for u in get_all_users()}
        anoushka = users["S26CSEU1922"]
        srishthi = users["S26CSEU1939"]

        month = "2026-11"
        # Anoushka sets budget for Books & Supplies
        set_user_monthly_budget(
            user_id=anoushka["id"],
            month_str=month,
            total_budget=5000.0,
            category_budgets={"Books & Supplies": 4500.0}
        )

        # Srishthi sets budget for Books & Supplies with different limit
        set_user_monthly_budget(
            user_id=srishthi["id"],
            month_str=month,
            total_budget=3000.0,
            category_budgets={"Books & Supplies": 1500.0}
        )

        # Query isolated budgets
        anoushka_budget = get_user_monthly_budget(user_id=anoushka["id"], month_str=month)
        srishthi_budget = get_user_monthly_budget(user_id=srishthi["id"], month_str=month)

        self.assertEqual(anoushka_budget["categories"].get("Books & Supplies"), 4500.0)
        self.assertEqual(srishthi_budget["categories"].get("Books & Supplies"), 1500.0)
        self.assertEqual(anoushka_budget["monthly_total"], 5000.0)
        self.assertEqual(srishthi_budget["monthly_total"], 3000.0)

    def test_account_deactivation_blocks_login(self):
        """Verify deactivating an account immediately blocks login."""
        users = {u["enrollment_no"]: u for u in get_all_users()}
        aatirth = users["S26CSEU1913"]
        admin = users["S26CSEU1935"]

        # Deactivate
        set_user_active_status(aatirth["id"], False, admin_user_id=admin["id"])

        # Attempt login - must fail
        self.assertIsNone(authenticate_user("S26CSEU1913", "Aatirth@1913"))

        # Reactivate
        set_user_active_status(aatirth["id"], True, admin_user_id=admin["id"])

        # Attempt login - must succeed
        self.assertIsNotNone(authenticate_user("S26CSEU1913", "Aatirth@1913"))

    def test_password_update_and_audit_logging(self):
        """Verify updating a user password and audit trail logging."""
        users = {u["enrollment_no"]: u for u in get_all_users()}
        ridhima = users["S26CSEU1925"]
        admin = users["S26CSEU1935"]

        # Change password
        new_pin = "Ridhima@2026New!"
        update_user_password(ridhima["id"], new_pin, admin_user_id=admin["id"])

        # Old password must fail
        self.assertIsNone(authenticate_user("S26CSEU1925", "Ridhima@1925"))

        # New password must succeed
        user = authenticate_user("S26CSEU1925", new_pin)
        self.assertIsNotNone(user)

        # Reset back to default PIN for consistency
        update_user_password(ridhima["id"], "Ridhima@1925", admin_user_id=admin["id"])
        self.assertIsNotNone(authenticate_user("S26CSEU1925", "Ridhima@1925"))

        # Verify audit logs captured the password reset events
        logs = get_audit_logs(limit=20)
        self.assertTrue(len(logs) > 0)
        action_types = [l["action"] for l in logs]
        self.assertIn("PASSWORD_UPDATED", action_types)

    def test_login_name_validation(self):
        """Verify login validates full name against the registered roster."""
        from modules.database import validate_login_credentials
        
        # Valid enrollment with matching full name
        valid, msg, user = validate_login_credentials(
            enrollment_no="S26CSEU1935",
            password="Harsh@1935",
            full_name="HARSH"
        )
        self.assertTrue(valid)
        self.assertIsNotNone(user)
        self.assertEqual(user["enrollment_no"], "S26CSEU1935")

        # Valid enrollment with partial matching full name (e.g. Harsh Raj)
        valid2, msg2, user2 = validate_login_credentials(
            enrollment_no="S26CSEU1935",
            password="Harsh@1935",
            full_name="Harsh Raj"
        )
        self.assertTrue(valid2)

        # Valid enrollment with completely mismatched full name (e.g. Ridhima entered for Harsh)
        valid_mismatch, msg_mismatch, user_mismatch = validate_login_credentials(
            enrollment_no="S26CSEU1935",
            password="Harsh@1935",
            full_name="Ridhima"
        )
        self.assertFalse(valid_mismatch)
        self.assertIsNone(user_mismatch)
        self.assertIn("Full Name does not match", msg_mismatch)

    def test_sample_demo_dataset_loading_and_isolation(self):
        """
        Verify sample demo dataset loads under the correct user,
        remains strictly isolated, and never leaks to other members.
        """
        from modules.sample_data import load_sample_dataset, has_sample_dataset, remove_user_sample_dataset
        users = {u["enrollment_no"]: u for u in get_all_users()}
        aatirth = users["S26CSEU1913"]
        srishthi = users["S26CSEU1939"]

        # Clean any prior demo data for both
        remove_user_sample_dataset(user_id=aatirth["id"])
        remove_user_sample_dataset(user_id=srishthi["id"])

        # Srishthi initially has 0 demo records
        self.assertEqual(has_sample_dataset(user_id=srishthi["id"]), 0)

        # Aatirth loads sample demo data
        res = load_sample_dataset(user_id=aatirth["id"], replace_existing=True)
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["transactions_loaded"], 0)

        # Aatirth now has demo records
        aatirth_demo_count = has_sample_dataset(user_id=aatirth["id"])
        self.assertEqual(aatirth_demo_count, res["transactions_loaded"])

        # Srishthi MUST STILL have 0 demo records (Strict Row-Level Isolation)
        self.assertEqual(has_sample_dataset(user_id=srishthi["id"]), 0)

        # Duplicate load attempt with replace_existing=False must return already_exists
        dup_res = load_sample_dataset(user_id=aatirth["id"], replace_existing=False)
        self.assertEqual(dup_res["status"], "already_exists")
        self.assertEqual(dup_res["count"], aatirth_demo_count)

    def test_demo_data_removal_preserves_genuine_transactions(self):
        """
        Verify removing demo data removes ONLY demo records and
        strictly preserves genuine user transactions.
        """
        from modules.sample_data import load_sample_dataset, remove_user_sample_dataset
        users = {u["enrollment_no"]: u for u in get_all_users()}
        anoushka = users["S26CSEU1922"]

        # 1. Clean prior demo data
        remove_user_sample_dataset(user_id=anoushka["id"])

        # 2. Add genuine transaction for Anoushka
        ok_gen, gen_id = add_user_transaction(
            user_id=anoushka["id"],
            t_date="2026-11-18",
            t_type="Expense",
            category="Education",
            amount=850.0,
            payment_mode="UPI (GPay / PhonePe / Paytm)",
            description="Genuine College Textbook Purchase",
            is_demo=0
        )
        self.assertTrue(ok_gen)

        # 3. Load sample demo dataset for Anoushka
        demo_res = load_sample_dataset(user_id=anoushka["id"], replace_existing=True)
        self.assertEqual(demo_res["status"], "success")

        # 4. Remove ONLY demo records
        del_res = remove_user_sample_dataset(user_id=anoushka["id"])
        self.assertEqual(del_res["status"], "success")
        self.assertEqual(del_res["deleted"], demo_res["transactions_loaded"])

        # 5. Verify genuine transaction is 100% PRESERVED
        user_txns = get_user_transactions(user_id=anoushka["id"])
        user_txn_ids = [t["id"] for t in user_txns]
        self.assertIn(gen_id, user_txn_ids)
        self.assertEqual(len(user_txns), 1)
        self.assertEqual(user_txns[0]["description"], "Genuine College Textbook Purchase")

        # Clean up genuine test record
        delete_user_transaction(user_id=anoushka["id"], txn_id=gen_id)

    def test_multi_user_csv_export_isolation(self):
        """Verify CSV export exports strictly the requested user's transactions."""
        from modules.data_manager import export_transactions_csv
        users = {u["enrollment_no"]: u for u in get_all_users()}
        ridhima = users["S26CSEU1925"]
        harsh = users["S26CSEU1935"]

        # Add private record for Ridhima
        ok_r, r_id = add_user_transaction(
            user_id=ridhima["id"],
            t_date="2026-11-18",
            t_type="Expense",
            category="Shopping",
            amount=1999.0,
            description="Ridhima Private Purchase"
        )
        # Add private record for Harsh
        ok_h, h_id = add_user_transaction(
            user_id=harsh["id"],
            t_date="2026-11-18",
            t_type="Income",
            category="Freelance / Gig",
            amount=15000.0,
            description="Harsh Private Freelance"
        )

        # Export Ridhima's CSV
        r_csv = export_transactions_csv(user_id=ridhima["id"])
        self.assertIn("Ridhima Private Purchase", r_csv)
        self.assertNotIn("Harsh Private Freelance", r_csv)

        # Export Harsh's CSV
        h_csv = export_transactions_csv(user_id=harsh["id"])
        self.assertIn("Harsh Private Freelance", h_csv)
        self.assertNotIn("Ridhima Private Purchase", h_csv)

        # Cleanup
        delete_user_transaction(user_id=ridhima["id"], txn_id=r_id)
        delete_user_transaction(user_id=harsh["id"], txn_id=h_id)


if __name__ == "__main__":
    unittest.main()
