from __future__ import annotations
import os
from typing import Mapping, Any

def build_frozen_likelihood_display_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Upgraded 120-point Direct Injection Data Formatter.
    Integrates the aligned DESI DR2 120-point matrix into the global session context.
    """
    metadata = payload.get("metadata", {})
    derived = payload.get("derived", {})
    desi = payload.get("desi_dr2_bao", {})

    # 確定マウントされた120点リアルデータアセットの物理探索
    target_asset = "data/frozen_likelihood_asset/raw_injection/DESI_DR2_ALIGNED_120_MATRIX_20260720_020738_N.tsv"
    
    z_i_list = []
    y_i_list = []
    w_i_list = []
    matrix_status = "NOT_FOUND"
    asset_hash = "25a4e574544aabf12229d25eca00be8be28ee7142bbe1694c2095c8be6d1820a"

    if os.path.exists(target_asset):
        try:
            with open(target_asset, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("z") or not line.strip():
                        continue
                    parts = line.strip().split("\t")
                    if len(parts) == 3:
                        z_i_list.append(float(parts[0]))
                        y_i_list.append(float(parts[1]))
                        w_i_list.append(float(parts[2]))
            matrix_status = "ACTIVE_MOUNTED"
        except Exception:
            matrix_status = "LOAD_FAILED"

    # 下流のUI描画および jump_discontinuity_diagnostics.py が直接ハッシュ監査できるデータ構造へ拡張
    return {
        "case_id": metadata.get("case_id"),
        "provenance": metadata.get("provenance"),
        "rs_drag": derived.get("rs_drag"),
        "chi2": desi.get("chi2"),
        "loglike": desi.get("loglike"),
        "posterior": "NO" if matrix_status != "ACTIVE_MOUNTED" else "WOC_DTI_MUTED",
        "MCMC": "NO",
        "dti_120_grid": {
            "status": matrix_status,
            "target_asset": target_asset,
            "expected_sha256": asset_hash,
            "row_count": len(z_i_list),
            "z_i": z_i_list,
            "y_i": y_i_list,
            "w_i": w_i_list
        }
    }
