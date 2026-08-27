#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path

MOVIES_FILE = Path("data/movies_raw.json")
OUTPUT_FILE = Path("data/movies_rated.json")
WMDB_API = "https://api.wmdb.tv/api/v1/movie/search"

def fetch_rating(title):
    try:
        resp = requests.get(WMDB_API, params={"q": title, "limit": 1},
                           timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        if data and len(data) > 0:
            m = data[0]
            return {
                "rating": m.get("doubanRating", ""),
                "poster": m.get("img", "")
            }
    except:
        pass
    return {}

def main():
    movies = json.loads(MOVIES_FILE.read_text(encoding="utf-8"))
    total = len(movies)
    print(f"为 {total} 部影片补充评分...")
    
    for i, movie in enumerate(movies):
        name = movie["vod_name"]
        if name:
            info = fetch_rating(name)
            movie["rating"] = info.get("rating", "")
            if info.get("poster"):
                movie["vod_pic"] = info["poster"]
        
        if (i + 1) % 50 == 0:
            print(f"  进度: {i+1}/{total}")
            OUTPUT_FILE.write_text(
                json.dumps(movies[:i+1], ensure_ascii=False, indent=2),
                encoding="utf-8")
        time.sleep(0.3)
    
    OUTPUT_FILE.write_text(
        json.dumps(movies, ensure_ascii=False, indent=2), encoding="utf-8")
    rated = sum(1 for m in movies if m.get("rating"))
    print(f"完成: {rated}/{total} 有评分")

if __name__ == "__main__":
    main()
