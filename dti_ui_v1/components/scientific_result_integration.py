from dti_ui_v1.services.scientific_result_binding import (
    load_result_binding,
)

from dti_ui_v1.components.scientific_result_panel import (
    render_scientific_result_panel,
)


def build_scientific_display_context(source_path):
    return load_result_binding(source_path)


def render_scientific_display(source_path):
    payload = build_scientific_display_context(source_path)
    render_scientific_result_panel(payload)
    return payload
