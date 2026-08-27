#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

CMS_SITES = Path("sources/cms_sites.json")
OUTPUT_DIR = Path("data")
MOVIES_FILE = OUTPUT_DIR / "movies_raw.json"

def fetch_movie_list(api_base, page=1, limit=30):
    try:
        resp = requests.get(api_base,
            params={"ac": "detail", "pg": page, "limit": limit},
            timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        return data.get("list", []), data.get("pagecount", 1)
    except:
        return [], 1

def crawl_single_site(site):
    api = site["api"]
    name = site["name"]
    all_movies = []
    
    for pg in range(1, 6):
        movies, page_count = fetch_movie_list(api, page=pg, limit=30)
        all_movies.extend(movies)
        if pg >= page_count:
            break
        time.sleep(0.3)
    
    seen = set()
    unique = []
    for m in all_movies:
        vid = m.get("vod_id")
        if vid and vid not in seen:
            seen.add(vid)
            unique.append(m)
    
    print(f"  {name}: {len(unique)} 部")
    return unique

def normalize(movie, source):
    return {
        "vod_id": movie.get("vod_id"),
        "vod_name": movie.get("vod_name", "").strip(),
        "vod_year": movie.get("vod_year", ""),
        "vod_area": movie.get("vod_area", ""),
        "vod_remarks": movie.get("vod_remarks", ""),
        "vod_pic": movie.get("vod_pic", ""),
        "vod_class": movie.get("vod_class", ""),
        "vod_content": movie.get("vod_content", "")[:200],
        "source": source
    }

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sites = json.loads(CMS_SITES.read_text(encoding="utf-8"))
    
    all_movies = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(crawl_single_site, s): s for s in sites}
        for future in as_completed(futures):
            site = futures[future]
            try:
                movies = future.result()
                for m in movies:
                    all_movies.append(normalize(m, site["name"]))
            except Exception as e:
                print(f"  {site['name']}: 失败 {e}")
    
    seen_names = set()
    unique = []
    for m in all_movies:
        name = m["vod_name"]
        if name and name not in seen_names:
            seen_names.add(name)
            unique.append(m)
    
    MOVIES_FILE.write_text(
        json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n共获取 {len(unique)} 部不重复影片")

if __name__ == "__main__":
    main()
