#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

MOVIES_FILE = Path("data/movies_rated.json")
TEMPLATE_FILE = Path("tvbox.json")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "tvbox.json"

GH_PROXY = "https://ghfast.top"

SPIDER_URL = f"{GH_PROXY}/https://raw.githubusercontent.com/fish2018/tvbox/master/jar/json无敌.jar"

def generate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    movies = json.loads(MOVIES_FILE.read_text(encoding="utf-8"))
    config = json.loads(TEMPLATE_FILE.read_text(encoding="utf-8"))
    
    movies.sort(key=lambda x: float(x.get("rating") or 0), reverse=True)
    
    (OUTPUT_DIR / "movies.json").write_text(
        json.dumps(movies, ensure_ascii=False, indent=2), encoding="utf-8")
    
    movies_url = f"{GH_PROXY}/raw.githubusercontent.com/yangclaw2026-png/my-tvbox/main/output/movies.json"
    
    config["spider"] = SPIDER_URL
    config["sites"] = [{
        "key": "my_library",
        "name": "我的影视库",
        "type": 4,
        "api": movies_url,
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
