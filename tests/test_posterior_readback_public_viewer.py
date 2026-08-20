from __future__ import annotations

import unittest

from dti_ui_v1.services.posterior_readback_public_viewer import (
    FINAL_HANDOVER_ZIP_SHA256,
    POSTERIOR_READBACK_PLOTS,
    public_asset_manifest,
    public_viewer_rows,
    resolved_asset_path,
)


class PosteriorReadbackPublicViewerTests(unittest.TestCase):
    def test_public_viewer_keeps_five_internal_plot_roles(self) -> None:
        self.assertEqual([asset.plot_id for asset in POSTERIOR_READBACK_PLOTS], ["P1", "P2", "P3", "P4", "P5"])
        self.assertEqual(
            [asset.internal_role for asset in POSTERIOR_READBACK_PLOTS],
            ["primary", "primary", "secondary", "secondary", "reference-only"],
        )

    def test_public_viewer_boundary_has_no_posterior_claims(self) -> None:
        rows = public_viewer_rows()

        self.assertEqual(len(rows), 5)
        self.assertEqual(
            FINAL_HANDOVER_ZIP_SHA256,
            "22f3194eb17524cc92bb01604a53d1b1e13345ec21d33934bbaed01255702b21",
        )
        for row in rows:
            self.assertIn("not", row["Boundary"].lower())
            self.assertIn(row["Public image bundled"], {"YES", "NO"})
            self.assertTrue(row["Public asset path"].startswith("assets/posterior_readback_public_viewer/"))

    def test_public_viewer_assets_are_bundled_with_manifest_sha(self) -> None:
        manifest = public_asset_manifest()
        self.assertEqual(
            manifest["asset_manifest_schema"],
            "dti-posterior-readback-public-assets-v1",
        )
        self.assertIn("no_mcmc_rerun", manifest["source_policy"])

        rows = public_viewer_rows()
        self.assertEqual({row["Public image bundled"] for row in rows}, {"YES"})
        for row in rows:
            self.assertEqual(len(row["SHA256"]), 64)

        for asset in POSTERIOR_READBACK_PLOTS:
            path = resolved_asset_path(asset)
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 10_000)


if __name__ == "__main__":
    unittest.main()
