from pathlib import Path
import json
import datetime


def save_result(result):

    root=Path(
        "data/research/evidence/dti_raw_profile/results"
    )

    root.mkdir(
        parents=True,
        exist_ok=True
    )

    out=root/"route_a_gtds_latest.json"

    payload={

        "created":
            str(datetime.datetime.now()),

        "result":
            result

    }

    out.write_text(
        json.dumps(
            payload,
            indent=2
        )
    )

    return out
