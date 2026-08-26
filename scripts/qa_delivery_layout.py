from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from openpyxl import load_workbook
except ImportError as exc:
    raise SystemExit("需要 Python 3 和 openpyxl 才能运行此验证器") from exc


VALID_ROLES = {"feature", "shared", "referenced"}


def normalized(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path.resolve())))


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 Bubble 配置表的输出路径与工作簿聚合")
    parser.add_argument("manifest", type=Path, help="generation-manifest.json")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"交付清单不存在: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    def add(bucket, code: str, message: str, **details):
        bucket.append({"code": code, "message": message, **details})

    resolved_value = data.get("resolved_output_directory")
    if not resolved_value:
        add(errors, "MISSING_OUTPUT_DIRECTORY", "缺少resolved_output_directory")
        output_dir = manifest_path.parent
    else:
        output_dir = Path(resolved_value).expanduser().resolve()
        if not output_dir.is_dir():
            add(errors, "OUTPUT_DIRECTORY_NOT_FOUND", "实际输出目录不存在", path=str(output_dir))

    if normalized(manifest_path.parent) != normalized(output_dir):
        add(errors, "MANIFEST_OUTSIDE_OUTPUT_DIRECTORY", "generation-manifest.json必须位于实际输出目录", manifest=str(manifest_path), output_directory=str(output_dir))

    requested_value = data.get("requested_output_path")
    requested_path = Path(requested_value).expanduser().resolve() if requested_value else None
    if requested_path:
        expected_dir = requested_path.parent if requested_path.suffix.lower() == ".xlsx" else requested_path
        if normalized(expected_dir) != normalized(output_dir):
            add(errors, "OUTPUT_PATH_MISMATCH", "实际输出目录与用户指定路径不一致", requested=str(requested_path), actual=str(output_dir))

    feature_key = str(data.get("feature_key") or "").strip()
    if not feature_key:
        add(errors, "MISSING_FEATURE_KEY", "缺少feature_key，无法判断同功能工作簿是否碎片化")

    workbooks = data.get("workbooks")
    if not isinstance(workbooks, list) or not workbooks:
        add(errors, "MISSING_WORKBOOK_PLAN", "workbooks必须是非空数组")
        workbooks = []

    feature_entries = []
    seen_paths: set[str] = set()
    declared_sheets: dict[str, str] = {}

    for index, entry in enumerate(workbooks):
        if not isinstance(entry, dict):
            add(errors, "BAD_WORKBOOK_ENTRY", "工作簿条目必须是对象", index=index)
            continue
        role = entry.get("role")
        if role not in VALID_ROLES:
            add(errors, "BAD_WORKBOOK_ROLE", "role必须为feature/shared/referenced", index=index, role=role)
        if role == "feature":
            feature_entries.append(entry)
            if entry.get("feature_key") != feature_key:
                add(errors, "FEATURE_KEY_MISMATCH", "主功能工作簿的feature_key与清单不一致", index=index)
        elif not str(entry.get("reason") or "").strip():
            add(errors, "MISSING_EXCEPTION_REASON", "公共或引用工作簿必须说明归属依据", index=index)

        raw_path = entry.get("path")
        if not raw_path:
            add(errors, "MISSING_WORKBOOK_PATH", "工作簿条目缺少path", index=index)
            continue
        candidate = Path(raw_path).expanduser()
        workbook_path = candidate.resolve() if candidate.is_absolute() else (output_dir / candidate).resolve()
        path_key = normalized(workbook_path)
        if path_key in seen_paths:
            add(errors, "DUPLICATE_WORKBOOK_ENTRY", "同一工作簿在清单中重复出现", path=str(workbook_path))
        seen_paths.add(path_key)
        if workbook_path.suffix.lower() != ".xlsx":
            add(errors, "BAD_WORKBOOK_EXTENSION", "配置工作簿必须为xlsx", path=str(workbook_path))
        if normalized(workbook_path.parent) != normalized(output_dir):
            add(errors, "WORKBOOK_OUTSIDE_OUTPUT_DIRECTORY", "最终工作簿不在用户输出目录中", path=str(workbook_path))
        if not workbook_path.is_file():
            add(errors, "WORKBOOK_NOT_FOUND", "清单声明的工作簿不存在", path=str(workbook_path))
            continue

        sheets = entry.get("sheets")
        if not isinstance(sheets, list) or not sheets:
            add(errors, "MISSING_SHEET_LIST", "工作簿条目必须声明本次新增或修改的Sheet", path=str(workbook_path))
            continue
        wb = load_workbook(workbook_path, read_only=True, data_only=False)
        actual_sheets = set(wb.sheetnames)
        wb.close()
        for sheet in sheets:
            if sheet not in actual_sheets:
                add(errors, "SHEET_NOT_FOUND", "清单声明的Sheet不在工作簿中", path=str(workbook_path), sheet=sheet)
            previous = declared_sheets.get(sheet)
            if previous and previous != path_key:
                add(errors, "SHEET_SPLIT_ACROSS_WORKBOOKS", "同一Sheet被分配到多个工作簿", sheet=sheet)
            declared_sheets[sheet] = path_key

    if len(feature_entries) != 1:
        add(errors, "FEATURE_WORKBOOK_FRAGMENTATION", "同一个feature_key必须且只能有一个主功能工作簿", feature_key=feature_key, feature_workbook_count=len(feature_entries))

    if requested_path and requested_path.suffix.lower() == ".xlsx" and len(feature_entries) == 1:
        feature_raw = Path(feature_entries[0]["path"]).expanduser()
        feature_path = feature_raw.resolve() if feature_raw.is_absolute() else (output_dir / feature_raw).resolve()
        if normalized(feature_path) != normalized(requested_path):
            add(errors, "FEATURE_FILENAME_MISMATCH", "主功能工作簿没有使用用户指定的完整xlsx路径", requested=str(requested_path), actual=str(feature_path))

    report = {
        "ok": not errors,
        "manifest": str(manifest_path),
        "resolved_output_directory": str(output_dir),
        "feature_key": feature_key,
        "workbook_count": len(workbooks),
        "feature_workbook_count": len(feature_entries),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }
    sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
