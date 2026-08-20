from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


FINAL_HANDOVER_ID = "DTI_POST_OPTIMIZER_MCMC_POSTERIOR_READBACK_INTERNAL_FINAL_HANDOVER_V1"
FINAL_HANDOVER_ZIP_SHA256 = (
    "22f3194eb17524cc92bb01604a53d1b1e13345ec21d33934bbaed01255702b21"
)
PUBLIC_VIEWER_ASSET_ROOT = Path("assets/posterior_readback_public_viewer")
PUBLIC_VIEWER_ASSET_MANIFEST = PUBLIC_VIEWER_ASSET_ROOT / "POSTERIOR_READBACK_PUBLIC_ASSET_MANIFEST.json"


@dataclass(frozen=True)
class PosteriorReadbackPlotAsset:
    plot_id: str
    internal_role: str
    title: str
    boundary: str
    asset_filename: str

    @property
    def relative_path(self) -> Path:
        return PUBLIC_VIEWER_ASSET_ROOT / self.asset_filename


POSTERIOR_READBACK_PLOTS: tuple[PosteriorReadbackPlotAsset, ...] = (
    PosteriorReadbackPlotAsset(
        plot_id="P1",
        internal_role="primary",
        title="Internal corner-pair geometry sketch",
        boundary="Internal diagnostic only; not a public posterior constraint or confidence region.",
        asset_filename="P1_internal_corner_pair_geometry.png",
    ),
    PosteriorReadbackPlotAsset(
        plot_id="P2",
        internal_role="primary",
        title="Internal correlation heatmap",
        boundary="Internal correlation structure only; not model validation or public posterior evidence.",
        asset_filename="P2_internal_correlation_heatmap.png",
    ),
    PosteriorReadbackPlotAsset(
        plot_id="P3",
        internal_role="secondary",
        title="Internal median and quantile table figure",
        boundary="Internal readback only; not publication confidence intervals or final parameter constraints.",
        asset_filename="P3_internal_median_quantile_table.png",
    ),
    PosteriorReadbackPlotAsset(
        plot_id="P4",
        internal_role="secondary",
        title="Internal component chi2 distribution figure",
        boundary="Internal component summary only; not a likelihood rerun, evidence comparison, or model comparison.",
        asset_filename="P4_internal_component_chi2_distribution.png",
    ),
    PosteriorReadbackPlotAsset(
        plot_id="P5",
        internal_role="reference-only",
        title="Internal best sampled diagnostic marker figure",
        boundary="Reference-only sampled diagnostic row; not a global, optimizer, final, or publication best fit.",
        asset_filename="P5_internal_best_sampled_marker.png",
    ),
)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolved_asset_path(asset: PosteriorReadbackPlotAsset) -> Path:
    return repository_root() / asset.relative_path


def public_asset_manifest() -> dict[str, object]:
    path = repository_root() / PUBLIC_VIEWER_ASSET_MANIFEST
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _manifest_sha_by_plot() -> dict[str, str]:
    manifest = public_asset_manifest()
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return {}
    rows: dict[str, str] = {}
    for item in assets:
        if not isinstance(item, dict):
            continue
        plot_id = item.get("plot_id")
        sha256 = item.get("sha256")
        if isinstance(plot_id, str) and isinstance(sha256, str):
            rows[plot_id] = sha256
    return rows


def public_viewer_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    sha_by_plot = _manifest_sha_by_plot()
    for asset in POSTERIOR_READBACK_PLOTS:
        path = resolved_asset_path(asset)
        rows.append(
            {
                "Plot": asset.plot_id,
                "Internal role": asset.internal_role,
                "Public image bundled": "YES" if path.is_file() else "NO",
                "Public asset path": str(asset.relative_path),
                "SHA256": sha_by_plot.get(asset.plot_id, ""),
                "Boundary": asset.boundary,
            }
        )
    return rows
