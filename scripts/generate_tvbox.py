#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

MOVIES_FILE = Path("data/movies_raw.json")
OUTPUT_DIR = Path("data")
CMS_FILE = OUTPUT_DIR / "movies_cms.json"

def generate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    movies = json.loads(MOVIES_FILE.read_text(encoding="utf-8"))
    
    movies.sort(key=lambda x: float(x.get("rating") or 0), reverse=True)
    
    categories = {}
    for m in movies:
        cls = m.get("vod_class") or "其他"
        if cls not in categories:
            categories[cls] = []
        categories[cls].append(m)
    
    class_list = []
    for i, (cls, mlist) in enumerate(categories.items(), 1):
        class_list.append({"type_id": i, "type_name": cls})
    
    vod_list = []
    for m in movies:
        cls = m.get("vod_class") or "其他"
        type_id = next((c["type_id"] for c in class_list if c["type_name"] == cls), 1)
        vod_list.append({
            "vod_id": m.get("vod_id", 0),
            "vod_name": m.get("vod_name", ""),
            "vod_pic": m.get("vod_pic", ""),
            "vod_year": m.get("vod_year", ""),
            "vod_area": m.get("vod_area", ""),
            "vod_remarks": m.get("vod_remarks", ""),
            "type_id": type_id,
            "type_name": cls,
            "vod_content": m.get("vod_content", ""),
            "vod_play_url": m.get("vod_play_url", ""),
            "vod_play_from": m.get("vod_play_from", ""),
            "source": m.get("source", "")
        })
    
    cms_data = {
        "code": 1,
        "msg": "数据列表",
        "page": 1,
        "pagecount": 1,
        "limit": len(vod_list),
        "total": len(vod_list),
        "list": vod_list,
        "class": class_list
    }
    
    CMS_FILE.write_text(
        json.dumps(cms_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"生成完成: {len(vod_list)} 部影片, {len(class_list)} 个分类")

if __name__ == "__main__":
    generate()
