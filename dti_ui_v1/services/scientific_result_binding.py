from pathlib import Path

from dti_ui_v1.services.scientific_result_adapter import (
    build_scientific_result_payload,
)


def load_result_binding(source_path):
    path = Path(source_path)

    return build_scientific_result_payload(
        source_path=str(path),
    )
