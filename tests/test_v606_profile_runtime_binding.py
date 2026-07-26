from __future__ import annotations

import os
import unittest
from pathlib import Path

from dti_ui_v1.services.v606_profile_adapter import (
    load_v606_profile_library,
)
from dti_ui_v1.services.v606_profile_runtime_binding import (
    OPTIONAL_UNBOUND_FIELDS,
    REFERENCE_ONLY_FIELDS,
    SESSION_KEY_MAP,
    V606ProfileRuntimeBindingError,
    apply_runtime_binding,
    prepare_runtime_binding,
)


class V606ProfileRuntimeBindingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = os.environ["V606_PROFILE_ARCHIVE"]
        expected_sha = os.environ["V606_PROFILE_ARCHIVE_SHA256"]

        cls.library = load_v606_profile_library(
            Path(source),
            expected_sha256=expected_sha,
            expected_count=100,
        )

    def test_known_profile_payload(self) -> None:
        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        self.assertEqual(
            binding.session_payload[
                "perfect_fit_general_class_H0_v1"
            ],
            67.36,
        )
        self.assertEqual(
            binding.session_payload[
                "perfect_fit_general_class_f_EDE_v2"
            ],
            0.0,
        )

    def test_only_four_direct_fields_are_bound(self) -> None:
        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        self.assertEqual(
            set(binding.session_payload),
            set(SESSION_KEY_MAP.values()),
        )
        self.assertEqual(len(binding.session_payload), 4)

    def test_reference_outputs_are_not_session_inputs(self) -> None:
        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        for field in REFERENCE_ONLY_FIELDS:
            self.assertIn(field, binding.reference_outputs)
            self.assertNotIn(field, binding.session_payload)

    def test_z_c_remains_unbound(self) -> None:
        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        self.assertEqual(
            binding.optional_unbound,
            OPTIONAL_UNBOUND_FIELDS,
        )
        self.assertFalse(
            any("z_c" in key for key in binding.session_payload)
        )

    def test_apply_changes_only_direct_session_keys(self) -> None:
        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        state = {
            "perfect_fit_general_class_z_c": "3.5",
            "unrelated_key": "preserve",
        }

        changed = apply_runtime_binding(state, binding)

        self.assertEqual(set(changed), set(SESSION_KEY_MAP.values()))
        self.assertEqual(
            state["perfect_fit_general_class_z_c"],
            "3.5",
        )
        self.assertEqual(state["unrelated_key"], "preserve")

    def test_unknown_profile_rejected(self) -> None:
        with self.assertRaises(V606ProfileRuntimeBindingError):
            prepare_runtime_binding(
                self.library,
                "PROFILE_DOES_NOT_EXIST",
            )


    def test_pending_binding_consumed_once(self) -> None:
        from dti_ui_v1.services.v606_profile_runtime_binding import (
            PENDING_SESSION_PAYLOAD_KEY,
            consume_pending_runtime_binding,
            queue_runtime_binding,
        )

        binding = prepare_runtime_binding(
            self.library,
            "Planck_2018_LCDM_Base",
        )

        state = {
            "perfect_fit_general_class_z_c_v2": 3500.0,
            "perfect_fit_general_class_n_s_v1": 0.9847,
        }

        queued = queue_runtime_binding(state, binding)

        self.assertEqual(len(queued), 4)
        self.assertIn(PENDING_SESSION_PAYLOAD_KEY, state)
        self.assertNotIn(
            "perfect_fit_general_class_H0_v1",
            state,
        )

        changed = consume_pending_runtime_binding(state)

        self.assertEqual(set(changed), set(binding.session_payload))
        self.assertNotIn(PENDING_SESSION_PAYLOAD_KEY, state)
        self.assertEqual(
            state["perfect_fit_general_class_H0_v1"],
            67.36,
        )
        self.assertEqual(
            state["perfect_fit_general_class_z_c_v2"],
            3500.0,
        )

        second = consume_pending_runtime_binding(state)
        self.assertEqual(second, ())


if __name__ == "__main__":
    unittest.main()
