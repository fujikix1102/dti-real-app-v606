import unittest

from dti_ui_v1.services.likelihood_binding_service import (
    load_likelihood_binding_payload,
)

from dti_ui_v1.components.likelihood_frozen_display import (
    build_frozen_likelihood_display_payload,
)


ASSET = (
    "data/frozen_likelihood_asset/"
    "ONE_POINT_LIKELIHOOD_RESULT.FROZEN.json"
)


class TestLikelihoodDisplayIntegration(unittest.TestCase):

    def test_binding_to_display_flow(self):

        payload = load_likelihood_binding_payload(
            ASSET
        )

        display = build_frozen_likelihood_display_payload(
            payload
        )

        self.assertEqual(
            display["case_id"],
            "S003"
        )

        self.assertIn(
            "provenance",
            display
        )

        self.assertEqual(
            display["posterior"],
            "WOC_DTI_MUTED"
        )

        self.assertEqual(
            display["MCMC"],
            "NO"
        )


if __name__ == "__main__":
    unittest.main()
