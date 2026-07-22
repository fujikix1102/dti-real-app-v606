from pathlib import Path
import json


def load_gtds_display_payload(
    lock_path
):

    lock=Path(lock_path)

    data=json.loads(
        lock.read_text()
    )

    return {

        "name":
        data.get(
            "name"
        ),

        "file_count":
        data.get(
            "file_count"
        ),

        "claim_boundary":
        data.get(
            "claim_boundary"
        ),

        "mode":
        "DISPLAY_ONLY"

    }
