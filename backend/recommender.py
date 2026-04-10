import json
import os
import random
from itertools import combinations

try:
    from .ai_copy import generate_combo_copy
    from .database import get_all_foods
except ImportError:
    from ai_copy import generate_combo_copy
    from database import get_all_foods

_FOODS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "foods.json")

with open(_FOODS_PATH, encoding="utf-8") as _f:
    _JSON_FOODS = json.load(_f)["foods"]


def _load_foods() -> list:
    db_foods = get_all_foods()
    return db_foods if db_foods else _JSON_FOODS


ALL_FOODS = _JSON_FOODS  # kept for module-level compat

_CUISINE_LABELS = {
    "fast_food": "速食",
    "japanese": "日式",
    "taiwanese": "台式",
    "convenience_store": "超商",
    "western": "西式",
    "dessert": "甜點",
}

_STYLE_WORDS = ["爽感", "放縱", "滿足", "享樂", "豪邁", "過癮"]

_FLAVOR_MAP = [
    (["beef"], "牛肉控必選"),
    (["spicy"], "嗜辣派首選"),
    (["boba", "tea"], "台式飲料控"),
    (["sushi", "sashimi"], "清爽日式風味"),
    (["fried", "sweet"], "鹹甜兼顧"),
    (["fried"], "炸物控的最愛"),
    (["comfort_food"], "療癒系首選"),
    (["fish"], "海鮮清爽路線"),
]


def _filter(foods, cuisine, exclude_tags):
    result = foods
    if cuisine and cuisine != "all":
        result = [f for f in result if f["cuisine"] == cuisine]
    if exclude_tags:
        result = [f for f in result if not any(t in f["tags"] for t in exclude_tags)]
    return result


def _by_role(foods):
    d = {"main": [], "side": [], "drink": [], "dessert": []}
    for f in foods:
        role = f.get("meal_role")
        if role in d:
            d[role].append(f)
    return d


def _combo_name(main):
    label = _CUISINE_LABELS.get(main["cuisine"], "美食")
    return f"{label}{random.choice(_STYLE_WORDS)}套餐"


def _combo_reason(items, total_cal, target_cal):
    diff = total_cal - target_cal
    if abs(diff) <= 100:
        range_text = "剛好命中目標熱量"
    elif diff > 0:
        range_text = f"比目標多 {diff} kcal，超值爽感"
    else:
        range_text = f"比目標少 {abs(diff)} kcal，稍微克制一點"

    tags_all = {t for item in items for t in item.get("tags", [])}
    flavor = "均衡美味"
    for tag_list, label in _FLAVOR_MAP:
        if any(t in tags_all for t in tag_list):
            flavor = label
            break

    return f"{flavor}，{range_text}。"


def _diverse(candidates, n):
    candidates.sort(key=lambda x: x["diff"])
    selected, used = [], set()
    for c in candidates:
        mid = c["items"][0]["id"]
        if mid in used:
            continue
        selected.append(c)
        used.add(mid)
        if len(selected) >= n:
            break
    return selected


def recommend(target_calories, cuisine="all", exclude_tags=None, include_drink=True, include_dessert=True, n=5):
    exclude_tags = exclude_tags or []
    foods = _filter(_load_foods(), cuisine, exclude_tags)
    roles = _by_role(foods)

    mains = roles["main"]
    sides = roles["side"]
    drinks = roles["drink"]
    desserts = roles["dessert"]

    # Supplement drinks/desserts from full pool if filtered pool is empty
    if not drinks and include_drink:
        drinks = _by_role(_filter(ALL_FOODS, "all", exclude_tags))["drink"]
    if not desserts and include_dessert:
        desserts = _by_role(_filter(ALL_FOODS, "all", exclude_tags))["dessert"]

    candidates = []

    for main in mains:
        # side combos: none, 1, or 2 (different items)
        side_opts = [[]] + [[s] for s in sides]
        if len(sides) >= 2:
            side_opts += [[a, b] for a, b in combinations(sides[:6], 2) if a["id"] != b["id"]]

        drink_opts = [None] + (drinks if include_drink else [])
        dessert_opts = [None] + (desserts if include_dessert else [])

        for sc in side_opts:
            for dk in drink_opts:
                for ds in dessert_opts:
                    items = [main] + sc + ([dk] if dk else []) + ([ds] if ds else [])
                    total = sum(i["calories"] for i in items)
                    diff = abs(total - target_calories)
                    if diff <= 300:
                        candidates.append({
                            "items": items,
                            "total_calories": total,
                            "total_price": sum(i["price_twd"] for i in items),
                            "diff": diff,
                        })

    results = []
    for combo in _diverse(candidates, n):
        items = combo["items"]
        ai = generate_combo_copy(items, combo["total_calories"], target_calories)
        results.append({
            "name": ai["name"] if ai else _combo_name(items[0]),
            "items": [
                {
                    "id": i["id"],
                    "name": i["name"],
                    "brand": i["brand"],
                    "calories": i["calories"],
                    "price_twd": i["price_twd"],
                    "meal_role": i["meal_role"],
                }
                for i in items
            ],
            "total_calories": combo["total_calories"],
            "total_price": combo["total_price"],
            "reason": ai["reason"] if ai else _combo_reason(items, combo["total_calories"], target_calories),
        })

    return results
