from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


FILES = {
    "Bubble配置表_AI生成规范.md": "bubble-config-standard.md",
    "Bubble配置表_全表目录.md": "table-catalog.md",
    "Bubble配置表_AI字段字典.json": "field-dictionary.json",
    "Bubble配置表_AI关系字典.json": "relation-dictionary.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    default_root = Path(__file__).resolve().parents[4]
    parser = argparse.ArgumentParser(description="同步 Bubble 配置表规范快照到技能包")
    parser.add_argument("--project-root", type=Path, default=default_root)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    source_dir = project_root / "策划" / "配置表"
    skill_root = Path(__file__).resolve().parents[1]
    reference_dir = skill_root / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)

    manifest_files = []
    for source_name, target_name in FILES.items():
        source = source_dir / source_name
        target = reference_dir / target_name
        if not source.is_file():
            raise FileNotFoundError(f"缺少规范源文件: {source}")
        shutil.copy2(source, target)
        manifest_files.append({
            "source": str(source),
            "target": str(target.relative_to(skill_root)),
            "bytes": target.stat().st_size,
            "sha256": sha256(target),
        })

    field_data = json.loads((reference_dir / "field-dictionary.json").read_text(encoding="utf-8"))
    relation_data = json.loads((reference_dir / "relation-dictionary.json").read_text(encoding="utf-8"))
    manifest = {
        "synced_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "schema_version": field_data.get("schema_version"),
        "source_summary": field_data.get("source_summary"),
        "high_confidence_relations": len(relation_data.get("high_confidence_relations", [])),
        "files": manifest_files,
    }
    (reference_dir / "snapshot-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
