import unittest

from dti_ui_v1.components.likelihood_frozen_display import (
    build_frozen_likelihood_display_payload,
)


class TestLikelihoodFrozenDisplay(unittest.TestCase):

    def test_display_mapping(self):

        payload = {
            "metadata": {
                "case_id": "S003",
                "provenance": {},
            },
            "derived": {
                "rs_drag": 142.88,
            },
            "desi_dr2_bao": {
                "chi2": 91.17,
                "loglike": -45.58,
            },
        }

        result = build_frozen_likelihood_display_payload(
            payload
        )

        self.assertEqual(
            result["case_id"],
            "S003"
        )

        self.assertEqual(
            result["posterior"],
            "WOC_DTI_MUTED"
        )

        self.assertEqual(
            result["MCMC"],
            "NO"
        )


if __name__ == "__main__":
    unittest.main()
