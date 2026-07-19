from __future__ import annotations

import copy
import unittest
from pathlib import Path

try:
    from dti_ui_v1.services.hubble_consistency_engine import (
        anchor_by_id,
        anchor_diagnostic,
        comparison_rows,
        load_anchor_contract,
        tradeoff_classification,
        validate_anchor_contract,
    )
except ImportError:
    from hubble_consistency_engine import (
        anchor_by_id,
        anchor_diagnostic,
        comparison_rows,
        load_anchor_contract,
        tradeoff_classification,
        validate_anchor_contract,
    )


CONTRACT_PATH = Path(__file__).with_name("hubble_ladder_anchors.json")
if not CONTRACT_PATH.is_file():
    CONTRACT_PATH = Path(__file__).resolve().parents[1] / "data" / "research" / "hubble_ladder_anchors.json"


def _response(desi: float, planck: float, pantheon: float) -> dict:
    return {
        "desi_dr2_bao": {"status": "ok", "chi2": desi},
        "planck_2018": {"status": "ok", "chi2_effective": planck},
        "pantheon_plus": {"status": "ok", "chi2": pantheon},
    }


class HubbleConsistencyEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_anchor_contract(CONTRACT_PATH)
        self.shoes = anchor_by_id(self.contract, "shoes_2022_cepheid_sn")

    def test_contract_has_unique_comparison_only_anchors(self) -> None:
        self.assertEqual(len(self.contract["anchors"]), 5)
        self.assertEqual(len({row["id"] for row in self.contract["anchors"]}), 5)
        self.assertTrue(all(row["joint_use_allowed"] is False for row in self.contract["anchors"]))

    def test_shoes_pull_coordinate(self) -> None:
        at_anchor = anchor_diagnostic(73.04, self.shoes)
        planck_like = anchor_diagnostic(67.4, self.shoes)
        self.assertAlmostEqual(float(at_anchor["pull_sigma"]), 0.0)
        self.assertAlmostEqual(float(planck_like["pull_sigma"]), (67.4 - 73.04) / 1.04)
        self.assertEqual(planck_like["band"], "beyond_3_sigma")

    def test_comparison_exposes_tradeoff_and_local_overlap(self) -> None:
        rows = comparison_rows(
            _response(10.0, 20.0, 30.0),
            _response(9.0, 21.0, 29.0),
            67.4,
            73.04,
            self.shoes,
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual(tradeoff_classification(rows), "CROSS_DATASET_TRADE_OFF")
        self.assertIn("overlaps Pantheon+", rows[-1]["combination"])

    def test_contract_rejects_joint_use(self) -> None:
        invalid = copy.deepcopy(self.contract)
        invalid.pop("contract_sha256", None)
        invalid["anchors"][0]["joint_use_allowed"] = True
        with self.assertRaises(ValueError):
            validate_anchor_contract(invalid)


if __name__ == "__main__":
    unittest.main()
