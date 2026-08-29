from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_DIR = ANALYSIS_DIR / "data"
DEFAULT_OUTPUT_PATH = ANALYSIS_DIR / "outputs" / "dataset.json"

FILE_NAMES = {
    "competitors": "organic-competitors.csv",
    "pages": "top-pages.csv",
    "keywords": "organic-keywords.csv",
}

EXPECTED_ROWS = {"competitors": 14, "pages": 406, "keywords": 409}

INTEGER_FIELDS = {
    "competitors": {
        "keywords_common",
        "keywords_competitor",
        "keywords_target",
        "traffic",
        "pages",
    },
    "pages": {
        "sum_traffic",
        "value",
        "keywords",
        "top_keyword_volume",
        "top_keyword_best_position",
        "referring_domains",
        "traffic_diff",
        "keywords_diff",
    },
    "keywords": {
        "volume",
        "keyword_difficulty",
        "cpc",
        "sum_traffic",
        "best_position",
        "words",
    },
}

FLOAT_FIELDS = {
    "competitors": {"share", "domain_rating"},
    "pages": {"ur"},
    "keywords": set(),
}

BOOLEAN_FIELDS = {
    "keywords": {
        "is_branded",
        "is_commercial",
        "is_informational",
        "is_navigational",
        "is_transactional",
        "is_local",
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tipa e reconcilia os três CSVs fornecidos no case."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Diretório dos três CSVs de origem.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Arquivo JSON de saída.",
    )
    return parser.parse_args()


def convert_value(dataset: str, field: str, value: str):
    if value == "":
        return None
    if field in INTEGER_FIELDS.get(dataset, set()):
        return int(value)
    if field in FLOAT_FIELDS.get(dataset, set()):
        return float(value)
    if field in BOOLEAN_FIELDS.get(dataset, set()):
        if value not in {"True", "False"}:
            raise ValueError(f"Booleano inesperado em {dataset}.{field}: {value!r}")
        return value == "True"
    return value


def read_dataset(dataset: str, path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Arquivo sem cabeçalho: {path}")
        headers = list(reader.fieldnames)
        rows = []
        for source_row, raw in enumerate(reader, start=2):
            typed = [convert_value(dataset, field, raw[field]) for field in headers]
            typed.append(source_row)
            rows.append(typed)
    return headers + ["source_row"], rows


def build_payload(source_dir: Path) -> dict:
    payload: dict = {"datasets": {}}
    all_domains = set()

    for dataset, file_name in FILE_NAMES.items():
        path = source_dir / file_name
        headers, rows = read_dataset(dataset, path)
        payload["datasets"][dataset] = {
            "source_file": file_name,
            "headers": headers,
            "rows": rows,
            "row_count": len(rows),
        }
        if "domain" in headers:
            domain_index = headers.index("domain")
            all_domains.update(row[domain_index] for row in rows)

    competitor_domains = {
        row[0] for row in payload["datasets"]["competitors"]["rows"]
    }
    actual_rows = {
        dataset: payload["datasets"][dataset]["row_count"] for dataset in FILE_NAMES
    }
    payload["domains"] = sorted(all_domains)
    payload["checks"] = {
        "competitor_domains": len(competitor_domains),
        "all_domains": len(all_domains),
        "expected_rows": EXPECTED_ROWS,
        "actual_rows": actual_rows,
        "row_counts_match": actual_rows == EXPECTED_ROWS,
    }
    return payload


def main() -> None:
    args = parse_args()
    payload = build_payload(args.source_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(args.output)


if __name__ == "__main__":
    main()
