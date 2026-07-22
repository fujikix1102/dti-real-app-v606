from pathlib import Path

from dti_ui_v1.services.scientific_result_binding import (
    load_result_binding,
)


def load_scientific_payload(source_path):
    path = Path(source_path)

    return load_result_binding(
        str(path)
    )
