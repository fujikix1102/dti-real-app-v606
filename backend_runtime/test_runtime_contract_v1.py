from backend_stub_runtime_v1 import (
    RuntimeBoundaryError,
    cache_boundary,
    cache_identity,
    cache_query,
    health,
    source_identity,
)

GOOD = {
    "cache_id": "synthetic_schema_only_probe_v1_cache",
    "query_mode": "identity",
    "allow_interpolation": False,
    "allow_extrapolation": False,
    "allow_silent_fallback": False,
    "claim_mode": "diagnostic_only",
}

def check(name, cond):
    if not cond:
        raise SystemExit(f"FAIL: {name}")
    print(f"PASS\t{name}")

def expect_error(name, payload, expected):
    try:
        cache_query(payload)
    except RuntimeBoundaryError as e:
        check(name, str(e) == expected)
        return
    raise SystemExit(f"FAIL: {name}: no error")

check("health_ok", health().status == "ok")
check("identity_ok", cache_identity().payload["cache_id"] == GOOD["cache_id"])
check("boundary_no_likelihood", cache_boundary().payload["boundary"]["likelihood"] == "NO")
check("source_no_raw_ingest", source_identity().payload["raw_desi_ingest"] is False)
check("query_identity_ok", cache_query(dict(GOOD)).status == "ok")

bad = dict(GOOD); bad["allow_interpolation"] = True
expect_error("reject_interpolation", bad, "FORBIDDEN_INTERPOLATION")
bad = dict(GOOD); bad["allow_extrapolation"] = True
expect_error("reject_extrapolation", bad, "FORBIDDEN_EXTRAPOLATION")
bad = dict(GOOD); bad["allow_silent_fallback"] = True
expect_error("reject_silent_fallback", bad, "FORBIDDEN_SILENT_FALLBACK")
bad = dict(GOOD); bad["claim_mode"] = "science"
expect_error("reject_claim_mode", bad, "CLAIM_BOUNDARY_TRIGGER")
bad = dict(GOOD); bad["query_mode"] = "likelihood"
expect_error("reject_query_mode", bad, "QUERY_MODE_FORBIDDEN")
bad = dict(GOOD); bad["cache_id"] = "other"
expect_error("reject_cache_id", bad, "CACHE_ID_MISMATCH")
