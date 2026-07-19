from __future__ import annotations

import unittest
from unittest.mock import patch

from dti_ui_v1.services import perfect_fit_compute_service as service
from dti_ui_v1.services.perfect_fit_http_transport import (
    post_json_transport,
)


class PerfectFitComputeServiceTests(unittest.TestCase):
    def test_injects_frozen_http_transport(self) -> None:
        captured: dict[str, object] = {}

        def fake_adapter(*args: object, **kwargs: object) -> object:
            captured["args"] = args
            captured["kwargs"] = kwargs
            return {"status": "fake-success"}

        with patch.object(
            service,
            "_adapter_entrypoint",
            fake_adapter,
        ):
            result = service.compute_perfect_fit(
                "positional-value",
                model="locked-baseline",
            )

        self.assertEqual(
            result,
            {"status": "fake-success"},
        )
        self.assertEqual(
            captured["args"],
            ("positional-value",),
        )

        delegated_kwargs = captured["kwargs"]
        self.assertIsInstance(delegated_kwargs, dict)
        self.assertEqual(
            delegated_kwargs["model"],
            "locked-baseline",
        )
        self.assertIs(
            delegated_kwargs[service._TRANSPORT_PARAMETER],
            post_json_transport,
        )

    def test_caller_cannot_override_transport(self) -> None:
        with self.assertRaisesRegex(
            TypeError,
            "controlled by perfect_fit_compute_service",
        ):
            service.compute_perfect_fit(
                **{
                    service._TRANSPORT_PARAMETER:
                    lambda *_args, **_kwargs: None,
                }
            )

    def test_adapter_exception_is_not_reinterpreted(self) -> None:
        expected = RuntimeError("adapter-failure")

        def fake_adapter(*args: object, **kwargs: object) -> object:
            raise expected

        with patch.object(
            service,
            "_adapter_entrypoint",
            fake_adapter,
        ):
            with self.assertRaises(RuntimeError) as caught:
                service.compute_perfect_fit(
                    timeout_seconds=10.0,
                )

        self.assertIs(caught.exception, expected)

    def test_caller_kwargs_are_not_mutated(self) -> None:
        caller_kwargs: dict[str, object] = {
            "timeout_seconds": 12.5,
            "use_locked_baseline": True,
        }

        captured: dict[str, object] = {}

        def fake_adapter(*args: object, **kwargs: object) -> object:
            captured.update(kwargs)
            return None

        original = dict(caller_kwargs)

        with patch.object(
            service,
            "_adapter_entrypoint",
            fake_adapter,
        ):
            service.compute_perfect_fit(**caller_kwargs)

        self.assertEqual(caller_kwargs, original)
        self.assertIs(
            captured[service._TRANSPORT_PARAMETER],
            post_json_transport,
        )


if __name__ == "__main__":
    unittest.main()
