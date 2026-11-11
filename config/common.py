
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
SEED = 42

for folder in [DATA / "processed", DATA / "teaching", REPORTS]:
    folder.mkdir(parents=True, exist_ok=True)

def save_json(filename, content):
    output = REPORTS / filename
    with open(output, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False, default=str)
