from __future__ import annotations

import unittest

from dti_ui_v1.components.general_class_compute_panel import (
    _GENERAL_CLASS_INPUT_DEFAULTS,
    _general_class_request_payload,
    _working_input_payload,
)


class GeneralClassComputePanelStateTests(unittest.TestCase):
    def test_request_payload_reads_current_session_state(self) -> None:
        state = dict(_GENERAL_CLASS_INPUT_DEFAULTS)
        state.update(
            {
                "perfect_fit_general_class_H0_v1": 73.0,
                "perfect_fit_general_class_omega_b_v1": 0.0224,
                "perfect_fit_general_class_omega_cdm_v1": 0.12,
                "perfect_fit_general_class_n_s_v1": 0.965,
                "perfect_fit_general_class_ln10_10_As_v1": 3.044,
                "perfect_fit_general_class_tau_reio_v1": 0.054,
                "perfect_fit_general_class_f_EDE_v2": 0.001,
                "perfect_fit_general_class_z_c_v2": 4000.0,
            }
        )

        payload = _general_class_request_payload(state)

        self.assertEqual(
            payload,
            {
                "H0": 73.0,
                "omega_b": 0.0224,
                "omega_cdm": 0.12,
                "n_s": 0.965,
                "ln10_10_As": 3.044,
                "tau_reio": 0.054,
                "f_EDE": 0.001,
                "z_c": 4000.0,
            },
        )

    def test_working_payload_retains_a_dti_without_forwarding_to_backend(self) -> None:
        state = dict(_GENERAL_CLASS_INPUT_DEFAULTS)
        state.update(
            {
                "perfect_fit_A_DTI_v1": 0.001,
                "perfect_fit_general_class_H0_v1": 68.0,
            }
        )

        backend_payload = _general_class_request_payload(state)
        working_payload = _working_input_payload(state)

        self.assertNotIn("A_DTI", backend_payload)
        self.assertEqual(working_payload["A_DTI"], 0.001)
        self.assertEqual(working_payload["H0"], 68.0)


if __name__ == "__main__":
    unittest.main()
