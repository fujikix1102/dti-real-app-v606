import json
from datetime import datetime


from dti_ui_v1.services.evidence_registry.evidence_chain_public_readiness_report import (
    build_public_readiness_report,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_health_status import (
    build_health_status,
)

from dti_ui_v1.services.evidence_registry.source_identity_registry import (
    build_source_identity_registry,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_diff_guard import (
    build_diff_guard,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_alert_router import (
    build_freeze_alerts,
)



def build_readiness_snapshot():

    registry = build_source_identity_registry()

    guard = build_diff_guard()

    alerts = build_freeze_alerts(
        guard
    )

    health = build_health_status()

    readiness = build_public_readiness_report()


    return {

        "snapshot_created":
            datetime.utcnow().isoformat()
            + "Z",

        "registry":
            registry,

        "freeze_guard":
            guard,

        "alerts":
            alerts,

        "health":
            health,

        "public_readiness":
            readiness,

        "boundary":
            {
                "likelihood": "NO",
                "posterior": "NO",
                "mcmc": "NO",
                "physical_claim": "NO",
            },

    }



def write_snapshot(path):

    snapshot = build_readiness_snapshot()

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            snapshot,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return snapshot
