#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

MOVIES_FILE = Path("data/movies_rated.json")
TEMPLATE_FILE = Path("tvbox.json")
OUTPUT_FILE = Path("output/tvbox.json")

def generate():
    movies = json.loads(MOVIES_FILE.read_text(encoding="utf-8"))
    config = json.loads(TEMPLATE_FILE.read_text(encoding="utf-8"))
    
    movies.sort(key=lambda x: float(x.get("rating") or 0), reverse=True)
    
    Path("output/movies.json").write_text(
        json.dumps(movies, ensure_ascii=False, indent=2), encoding="utf-8")
    
    config["sites"] = [{
        "key": "my_library",
        "name": "我的影视库",
        "type": 4,
        "api": "https://raw.githubusercontent.com/yangclaw2026-png/my-tvbox/main/output/movies.json",
        "searchable": 1,
        "quickSearch": 1,
        "filterable": 1
    }]
    config["_lastUpdate"] = datetime.now().isoformat()
    config["_totalMovies"] = len(movies)
    
    OUTPUT_FILE.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"生成完成: {len(movies)} 部影片")

if __name__ == "__main__":
    generate()
