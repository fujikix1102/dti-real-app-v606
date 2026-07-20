"""Public Streamlit entrypoint for the MAXOMEGA / DTI PERFECT FIT application."""

from pathlib import Path
import runpy

TARGET = Path(__file__).with_name("perfect_fit_app.py")

if not TARGET.is_file():
    raise FileNotFoundError(
        f"PERFECT FIT entrypoint was not found: {TARGET}"
    )

runpy.run_path(
    str(TARGET),
    run_name="__main__",
)
