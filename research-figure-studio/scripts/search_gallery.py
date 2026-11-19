"""Search SCI Figure Gallery metadata; download only the public JSON index."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import urlopen


INDEX_URL = "https://raw.githubusercontent.com/Chutj/sci-figure-gallery/main/data/gallery/public.json"
ALIASES = {
    "地图": "Maps", "折线图": "Lines, curves & time series",
    "时间序列": "Lines, curves & time series", "柱状图": "Bar charts",
    "散点图": "Scatter plots", "箱线图": "Box, violin & raincloud plots",
    "小提琴图": "Box, violin & raincloud plots", "雨云图": "Box, violin & raincloud plots",
    "示意图": "Schematics", "热力图": "Heatmaps & matrices",
    "密度图": "Density, ridgelines & cumulative distributions",
    "山脊图": "Density, ridgelines & cumulative distributions",
    "森林图": "Error bars, intervals & forest plots",
    "误差棒图": "Error bars, intervals & forest plots", "直方图": "Histograms",
    "模型评估": "Model evaluation", "网络图": "Paths & networks",
    "流程图": "Flowcharts & research frameworks",
    "技术路线图": "Flowcharts & research frameworks", "shap": "SHAP plots",
    "组成图": "Composition charts", "桑基图": "Sankey & chord diagrams",
    "弦图": "Sankey & chord diagrams", "极坐标图": "Polar plots",
    "等高线图": "Contours & response surfaces", "气泡图": "Bubble plots",
}


def read_index(path, refresh):
    if refresh or not path.exists():
        with urlopen(INDEX_URL, timeout=45) as response:
            content = response.read()
        data = json.loads(content)
        if not isinstance(data.get("records"), list):
            raise ValueError("Upstream index has no records list; inspect its current schema.")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    else:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    records = data.get("records")
    if not isinstance(records, list):
        raise ValueError("Index has no records list; inspect the supplied file.")
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True, help="Project-local metadata cache")
    parser.add_argument("--refresh", action="store_true", help="Download the current public index")
    parser.add_argument("--list-types", action="store_true")
    parser.add_argument("--type", default="", help="Chinese alias or unique English category substring")
    parser.add_argument("--query", default="", help="Space-separated terms; all must match metadata")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error("--limit must be between 1 and 30")
    if not (args.list_types or args.type or args.query):
        parser.error("Supply --list-types, --type, or --query")

    records = read_index(args.index, args.refresh)
    types = Counter(record["primary"] for record in records)
    result = {
        "index_source": INDEX_URL,
        "index_file": str(args.index.resolve()),
        "cache_modified_utc": datetime.fromtimestamp(args.index.stat().st_mtime, timezone.utc).isoformat(),
        "library_records": len(records),
    }
    if args.list_types:
        result["types"] = dict(types.most_common())
    else:
        selected_type = None
        if args.type:
            requested = ALIASES.get(args.type.casefold(), args.type).casefold()
            matches = [name for name in types if requested in name.casefold()]
            if len(matches) != 1:
                parser.error(f"Type must match one category; found {matches}. Use --list-types.")
            selected_type = matches[0]
        terms = args.query.casefold().split()
        candidates = []
        for record in records:
            if selected_type and record["primary"] != selected_type:
                continue
            searchable = " ".join([
                record.get("title", ""), record.get("paper", ""), record["primary"],
                " ".join(record.get("categories", [])),
                " ".join(record.get("sections", {}).values()),
            ]).casefold()
            if all(term in searchable for term in terms):
                candidates.append(record)
        fields = ("id", "title", "primary", "categories", "paper", "figure", "year", "source",
                  "image", "thumbnail", "sections")
        result.update({"selected_type": selected_type, "query": args.query,
                       "matched": len(candidates), "order": "upstream index order; not a quality ranking"})
        result["results"] = [
            {**{key: row.get(key) for key in fields},
             "rights": {key: row.get("rights", {}).get(key) for key in
                        ("license", "license_url", "status", "modification_status")},
             "gallery_url": "https://chutj.github.io/gallery/?" + urlencode({"figure": row["id"]})}
            for row in candidates[:args.limit]
        ]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
