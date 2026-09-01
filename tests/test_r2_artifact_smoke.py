from __future__ import annotations

from scripts.r2_artifact_smoke import _check_public_url


class _FakeResponse:
    def __init__(self, status_code: int, url: str = "https://example.test/") -> None:
        self.status_code = status_code
        self.url = url


def test_public_url_accepts_redirect_status_without_following(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_get(url: str, **kwargs):  # type: ignore[no-untyped-def]
        calls.append(kwargs)
        return _FakeResponse(303, url)

    monkeypatch.setattr("scripts.r2_artifact_smoke.requests.get", fake_get)

    result = _check_public_url("https://example.test/", timeout=1)

    assert result["checked"] is True
    assert result["ok"] is True
    assert result["status"] == 303
    assert result["reason"] == "redirect_not_followed"
    assert calls[0]["allow_redirects"] is False


def test_public_url_still_reports_non_redirect_errors(monkeypatch) -> None:
    def fake_get(url: str, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("connection refused")

    monkeypatch.setattr("scripts.r2_artifact_smoke.requests.get", fake_get)

    result = _check_public_url("https://example.test/", timeout=1)

    assert result["checked"] is True
    assert result["ok"] is False
    assert result["error"] == "connection refused"
