import os
from openai import OpenAI

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://hnd1.aihub.zeabur.ai/v1")
        if not api_key:
            return None
        _client = OpenAI(api_key=api_key, base_url=base_url)
    return _client


def generate_combo_copy(items: list, total_calories: int, target_calories: int) -> dict | None:
    """
    Use AI Hub to generate a creative name and reason for a meal combo.
    Returns {"name": ..., "reason": ...} or None if AI is unavailable.
    """
    client = _get_client()
    if not client:
        return None

    item_lines = "\n".join(
        f"- {i['name']}（{i['brand']}）{i['calories']} kcal，${i['price_twd']} TWD"
        for i in items
    )
    diff = total_calories - target_calories
    diff_text = (
        f"剛好命中目標（差 {abs(diff)} kcal）" if abs(diff) <= 100
        else f"比目標{'多' if diff > 0 else '少'} {abs(diff)} kcal"
    )

    prompt = f"""你是一個 cheat meal 推薦助手，幫用戶取餐點組合名稱和推薦理由。

餐點組合：
{item_lines}

總熱量：{total_calories} kcal（目標 {target_calories} kcal，{diff_text}）

請用繁體中文回覆，格式如下（只輸出這兩行，不要其他內容）：
名稱：<一句有爽感的組合名稱，10字以內>
理由：<一句推薦理由，帶點口語感，20字以內>"""

    try:
        model = os.getenv("AI_MODEL", "claude-sonnet-4-5")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8,
        )
        text = response.choices[0].message.content.strip()
        lines = {
            line.split("：", 1)[0]: line.split("：", 1)[1]
            for line in text.splitlines()
            if "：" in line
        }
        name = lines.get("名稱")
        reason = lines.get("理由")
        if name and reason:
            return {"name": name, "reason": reason}
    except Exception:
        pass

    return None
