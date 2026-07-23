"""
Future solver adapter boundary.

Runtime solver is intentionally not connected.
"""


def adapt_solver_response(response):
    """
    Converts validated solver response into display payload.

    This function does not call a solver.
    """

    return {
        "source": "runtime_solver",
        "payload": response,
        "frozen_payload": False,
    }
