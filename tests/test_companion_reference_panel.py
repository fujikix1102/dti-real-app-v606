from dti_ui_v1.components.companion_reference_panel import PUBLIC_APP_URL


def test_public_app_url_is_citation_target() -> None:
    assert PUBLIC_APP_URL == "https://dti-perfect-fit.streamlit.app/"
