from __future__ import annotations

from dti_ui_v1.app_shell import should_exclude_page_view_counter


def test_page_view_counter_exclusion_requires_configured_token() -> None:
    assert not should_exclude_page_view_counter(
        {"audit_view": "1", "token": "secret"},
        exclude_token="",
    )


def test_page_view_counter_exclusion_requires_audit_view_flag() -> None:
    assert not should_exclude_page_view_counter(
        {"token": "secret"},
        exclude_token="secret",
    )


def test_page_view_counter_exclusion_accepts_matching_token() -> None:
    assert should_exclude_page_view_counter(
        {"audit_view": "1", "token": "secret"},
        exclude_token="secret",
    )


def test_page_view_counter_exclusion_rejects_wrong_token() -> None:
    assert not should_exclude_page_view_counter(
        {"audit_view": "1", "token": "wrong"},
        exclude_token="secret",
    )
