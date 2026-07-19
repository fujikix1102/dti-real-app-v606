import unittest

from run_assumption_neutral_audit import run_audit


class AssumptionNeutralAuditTests(unittest.TestCase):
    def test_contract_and_conservative_conclusion(self):
        result = run_audit()
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["observed_compressed_product"]["representations_tested"], 4)
        self.assertFalse(result["machine_conclusion"]["compressed_product_proves_underlying_continuity"])
        self.assertFalse(result["machine_conclusion"]["observational_transition_detected"])
        self.assertGreater(result["injection_recovery"]["injected_replicates"], 0)
        self.assertFalse(result["catalog_pipeline"]["production_equivalent"])


if __name__ == "__main__":
    unittest.main()
