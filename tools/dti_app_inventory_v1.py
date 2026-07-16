#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


INPUT_METHODS = {
    "button",
    "checkbox",
    "color_picker",
    "date_input",
    "file_uploader",
    "multiselect",
    "number_input",
    "radio",
    "select_slider",
    "selectbox",
    "slider",
    "text_area",
    "text_input",
    "time_input",
    "toggle",
}

LAYOUT_METHODS = {
    "columns",
    "container",
    "dialog",
    "empty",
    "expander",
    "form",
    "popover",
    "sidebar",
    "tabs",
}

DISPLAY_METHODS = {
    "caption",
    "code",
    "data_editor",
    "dataframe",
    "error",
    "header",
    "image",
    "info",
    "json",
    "latex",
    "markdown",
    "metric",
    "plotly_chart",
    "pyplot",
    "subheader",
    "success",
    "table",
    "text",
    "title",
    "warning",
    "write",
}

API_NAMES = {
    "requests.get",
    "requests.post",
    "requests.put",
    "requests.patch",
    "requests.delete",
    "httpx.get",
    "httpx.post",
    "urllib.request.urlopen",
}

FILE_METHODS = {
    "open",
    "read_text",
    "read_bytes",
    "write_text",
    "write_bytes",
    "read_csv",
    "read_parquet",
    "read_json",
    "to_csv",
    "to_parquet",
    "to_json",
    "load",
    "loads",
    "dump",
    "dumps",
}

SECTION_PATTERN = re.compile(
    r"(?i)(section\s*\d+[a-z]?|route\s*[abc]|"
    r"source identity|provenance|fixed[- ]h0|"
    r"desi|bao|planck|stage\s*\d+|diagnostic|"
    r"public ui|runtime|audit|boundary)"
)


def write_rows(
    path: Path,
    headers: list[str],
    rows: Iterable[Iterable[Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.writer(
            handle,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writerow(headers)
        writer.writerows(rows)


def unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""

    try:
        return ast.unparse(node)
    except Exception:
        return ""


def literal(node: ast.AST | None) -> str:
    if node is None:
        return ""

    try:
        value = ast.literal_eval(node)
    except Exception:
        return unparse(node)

    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()

    return repr(value)


def function_name(node: ast.Call) -> str:
    return unparse(node.func)


def call_method(name: str) -> str:
    return name.rsplit(".", 1)[-1]


def call_category(name: str) -> str:
    method = call_method(name)

    if method in INPUT_METHODS:
        return "streamlit_input"

    if method in LAYOUT_METHODS:
        return "streamlit_layout"

    if method in DISPLAY_METHODS:
        return "streamlit_display"

    if method == "download_button":
        return "download"

    if name in API_NAMES:
        return "api_call"

    if method in FILE_METHODS:
        return "file_call"

    return "other"


def module_candidate(
    category: str,
    name: str,
    section: str,
    first_argument: str,
) -> str:
    text = (
        f"{category} {name} {section} {first_argument}"
    ).lower()

    if category == "api_call":
        return "services/api_client.py"

    if category == "file_call":
        return "services/data_access.py"

    if "provenance" in text or "identity" in text:
        return "components/identity_panel.py"

    if "boundary" in text or "forbidden" in text:
        return "components/boundary_notice.py"

    if call_method(name) in {
        "success",
        "warning",
        "error",
        "info",
    }:
        return "components/status_panel.py"

    if call_method(name) == "metric":
        return "components/numeric_metrics.py"

    if "physical bao" in text or "rdrag" in text:
        return "pages/physical_bao.py"

    if "route a" in text or "route b" in text:
        return "pages/route_ab.py"

    if "desi" in text:
        return "pages/desi_dr2.py"

    if "planck" in text:
        return "pages/planck.py"

    if category == "streamlit_input":
        return "components/inputs.py"

    if category == "streamlit_layout":
        return "components/layout.py"

    if category == "streamlit_display":
        return "components/display.py"

    return "pages/legacy_workspace.py"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    source = source_path.read_text(encoding="utf-8")
    source_lines = source.splitlines(keepends=True)
    tree = ast.parse(source)

    section_markers: list[tuple[int, str]] = []

    for number, text in enumerate(
        source.splitlines(),
        start=1,
    ):
        stripped = text.strip()

        if (
            stripped.startswith("#")
            and SECTION_PATTERN.search(stripped)
        ):
            section_markers.append(
                (
                    number,
                    stripped.lstrip("# ").strip(),
                )
            )

    def section_for(line: int) -> str:
        result = "<unsectioned>"

        for marker_line, marker_text in section_markers:
            if marker_line > line:
                break

            result = marker_text

        return result

    definitions: list[list[Any]] = []
    imports: list[list[Any]] = []
    calls: list[list[Any]] = []
    long_strings: defaultdict[str, list[int]] = defaultdict(list)

    parent_map: dict[ast.AST, ast.AST] = {}

    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    def enclosing_definition(node: ast.AST) -> str:
        names: list[str] = []
        current = parent_map.get(node)

        while current is not None:
            if isinstance(
                current,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                names.append(current.name)

            current = parent_map.get(current)

        return ".".join(reversed(names)) or "<module>"

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        ):
            end_line = node.end_lineno or node.lineno
            segment = "".join(
                source_lines[node.lineno - 1 : end_line]
            )

            if isinstance(node, ast.ClassDef):
                kind = "class"
                argument_count = 0
                decorators = node.decorator_list
            else:
                kind = (
                    "async_function"
                    if isinstance(node, ast.AsyncFunctionDef)
                    else "function"
                )
                argument_count = (
                    len(node.args.posonlyargs)
                    + len(node.args.args)
                    + len(node.args.kwonlyargs)
                )
                decorators = node.decorator_list

            definitions.append(
                [
                    kind,
                    node.name,
                    enclosing_definition(node),
                    node.lineno,
                    end_line,
                    end_line - node.lineno + 1,
                    len(decorators),
                    argument_count,
                    hashlib.sha256(
                        segment.encode("utf-8")
                    ).hexdigest(),
                ]
            )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    [
                        "import",
                        alias.name,
                        "",
                        alias.asname or "",
                        node.lineno,
                    ]
                )

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    [
                        "from_import",
                        node.module or "",
                        alias.name,
                        alias.asname or "",
                        node.lineno,
                    ]
                )

        elif isinstance(node, ast.Call):
            name = function_name(node)
            category = call_category(name)

            if category == "other":
                continue

            first_argument = (
                literal(node.args[0])
                if node.args
                else ""
            )

            keywords = ",".join(
                keyword.arg or "**"
                for keyword in node.keywords
            )

            section = section_for(node.lineno)

            calls.append(
                [
                    category,
                    name,
                    node.lineno,
                    node.col_offset,
                    enclosing_definition(node),
                    first_argument,
                    keywords,
                    section,
                    module_candidate(
                        category,
                        name,
                        section,
                        first_argument,
                    ),
                ]
            )

        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
        ):
            normalized = re.sub(
                r"\s+",
                " ",
                node.value,
            ).strip()

            if len(normalized) >= 12:
                long_strings[normalized].append(node.lineno)

    definitions.sort(key=lambda row: (int(row[3]), row[1]))
    imports.sort(key=lambda row: (int(row[4]), row[1]))
    calls.sort(key=lambda row: (int(row[2]), row[1]))

    inputs = [
        row
        for row in calls
        if row[0] == "streamlit_input"
    ]

    display_layout = [
        row
        for row in calls
        if row[0] in {
            "streamlit_display",
            "streamlit_layout",
            "download",
        }
    ]

    api_calls = [
        row
        for row in calls
        if row[0] == "api_call"
    ]

    file_calls = [
        row
        for row in calls
        if row[0] == "file_call"
    ]

    duplicate_strings = []

    for value, locations in long_strings.items():
        if len(locations) < 2:
            continue

        duplicate_strings.append(
            [
                value,
                len(locations),
                min(locations),
                len(value),
                ",".join(str(item) for item in locations),
                hashlib.sha256(
                    value.encode("utf-8")
                ).hexdigest(),
            ]
        )

    duplicate_strings.sort(
        key=lambda row: (
            -int(row[1]),
            -int(row[3]),
            int(row[2]),
        )
    )

    call_counter: Counter[tuple[str, str, str]] = Counter(
        (
            str(row[1]),
            str(row[5]),
            str(row[6]),
        )
        for row in calls
    )

    duplicate_calls = [
        [
            name,
            first_argument,
            keywords,
            count,
        ]
        for (
            name,
            first_argument,
            keywords,
        ), count in call_counter.items()
        if count > 1
    ]

    duplicate_calls.sort(
        key=lambda row: (
            -int(row[3]),
            row[0],
            row[1],
        )
    )

    section_counter = Counter(
        str(row[7])
        for row in calls
    )

    section_rows = [
        [
            section,
            next(
                (
                    line
                    for line, text in section_markers
                    if text == section
                ),
                0,
            ),
            count,
        ]
        for section, count in section_counter.most_common()
    ]

    module_counter = Counter(
        str(row[8])
        for row in calls
    )

    module_rows = [
        [module, count]
        for module, count in module_counter.most_common()
    ]

    definition_headers = [
        "kind",
        "name",
        "parent",
        "start_line",
        "end_line",
        "line_count",
        "decorator_count",
        "argument_count",
        "source_sha256",
    ]

    call_headers = [
        "category",
        "call_name",
        "line",
        "column",
        "enclosing_definition",
        "first_argument",
        "keyword_names",
        "section",
        "module_candidate",
    ]

    write_rows(
        output / "FUNCTION_INVENTORY.tsv",
        definition_headers,
        definitions,
    )

    write_rows(
        output / "IMPORT_INVENTORY.tsv",
        [
            "kind",
            "module",
            "name",
            "alias",
            "line",
        ],
        imports,
    )

    write_rows(
        output / "CLASSIFIED_CALLS.tsv",
        call_headers,
        calls,
    )

    write_rows(
        output / "INPUT_WIDGETS.tsv",
        call_headers,
        inputs,
    )

    write_rows(
        output / "DISPLAY_AND_LAYOUT.tsv",
        call_headers,
        display_layout,
    )

    write_rows(
        output / "API_CALLS.tsv",
        call_headers,
        api_calls,
    )

    write_rows(
        output / "FILE_ACCESS_CALLS.tsv",
        call_headers,
        file_calls,
    )

    write_rows(
        output / "SECTION_MARKERS.tsv",
        ["line", "text"],
        section_markers,
    )

    write_rows(
        output / "SECTION_MAP.tsv",
        [
            "section",
            "first_marker_line",
            "classified_call_count",
        ],
        section_rows,
    )

    write_rows(
        output / "MODULE_CANDIDATES.tsv",
        [
            "module_candidate",
            "referenced_call_count",
        ],
        module_rows,
    )

    write_rows(
        output / "DUPLICATE_STRINGS.tsv",
        [
            "value",
            "count",
            "first_line",
            "character_count",
            "lines",
            "normalized_sha256",
        ],
        duplicate_strings,
    )

    write_rows(
        output / "DUPLICATE_CALL_PATTERNS.tsv",
        [
            "call_name",
            "first_argument",
            "keyword_names",
            "count",
        ],
        duplicate_calls,
    )

    summary = {
        "source": str(source_path),
        "source_sha256": hashlib.sha256(
            source.encode("utf-8")
        ).hexdigest(),
        "source_lines": len(source.splitlines()),
        "source_bytes": len(source.encode("utf-8")),
        "definition_count": len(definitions),
        "import_count": len(imports),
        "classified_call_count": len(calls),
        "streamlit_input_count": len(inputs),
        "streamlit_display_layout_count": len(
            display_layout
        ),
        "api_call_count": len(api_calls),
        "file_call_count": len(file_calls),
        "section_marker_count": len(section_markers),
        "inferred_section_count": len(section_rows),
        "duplicate_string_group_count": len(
            duplicate_strings
        ),
        "duplicate_call_group_count": len(
            duplicate_calls
        ),
        "module_candidate_count": len(module_rows),
    }

    write_rows(
        output / "SUMMARY.tsv",
        ["key", "value"],
        summary.items(),
    )

    inventory = {
        "summary": summary,
        "definitions": definitions,
        "imports": imports,
        "calls": calls,
        "sections": section_rows,
        "section_markers": section_markers,
        "module_candidates": module_rows,
        "duplicate_strings": duplicate_strings,
        "duplicate_call_patterns": duplicate_calls,
    }

    (
        output / "INVENTORY.json"
    ).write_text(
        json.dumps(
            inventory,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    markdown = [
        "# DTI app.py inventory",
        "",
        f"- Source: `{source_path}`",
        f"- SHA256: `{summary['source_sha256']}`",
        f"- Lines: {summary['source_lines']}",
        f"- Definitions: {summary['definition_count']}",
        f"- Classified calls: {summary['classified_call_count']}",
        f"- Input widgets: {summary['streamlit_input_count']}",
        (
            "- Display/layout calls: "
            f"{summary['streamlit_display_layout_count']}"
        ),
        f"- API calls: {summary['api_call_count']}",
        f"- File calls: {summary['file_call_count']}",
        (
            "- Duplicate string groups: "
            f"{summary['duplicate_string_group_count']}"
        ),
        (
            "- Duplicate call groups: "
            f"{summary['duplicate_call_group_count']}"
        ),
        "",
        "## Module candidates",
        "",
        "| Module | Count |",
        "|---|---:|",
    ]

    for module, count in module_rows:
        markdown.append(f"| `{module}` | {count} |")

    (
        output / "SUMMARY.md"
    ).write_text(
        "\n".join(markdown) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
