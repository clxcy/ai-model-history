#!/usr/bin/env python3
"""转换数据并清理来源标记"""
import json

SRC = "D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布/models.json"
DST = "D:/WebDesign/ai-model-history/docs/models.json"

# 公司名 → logo 映射
EXTRA_LOGOS = {
    "openai": "https://github.com/openai.png",
    "google": "https://github.com/google.png",
    "anthropic": "https://github.com/anthropics.png",
    "meta": "https://github.com/facebook.png",
    "deepseek": "https://github.com/deepseek-ai.png",
    "mistral": "https://github.com/mistralai.png",
    "cohere": "https://github.com/cohere-ai.png",
    "microsoft": "https://github.com/microsoft.png",
    "nvidia": "https://github.com/nvidia.png",
    "阿里": "https://github.com/alibaba.png",
    "百度": "https://github.com/baidu.png",
    "腾讯": "https://github.com/tencent.png",
    "字节跳动": "https://github.com/bytedance.png",
    "智谱AI": "https://github.com/zhipuai.png",
    "月之暗面": "https://github.com/moonshotai.png",
    "minimax": "https://github.com/MiniMax-AI.png",
    "xai": "https://github.com/xai-org.png",
    "stability ai": "https://github.com/Stability-AI.png",
    "hugging face": "https://github.com/huggingface.png",
    "meta ai": "https://github.com/facebook.png",
}

def get_logo(company):
    if not company: return ""
    c = company.lower().strip()
    for key, url in EXTRA_LOGOS.items():
        if key in c or c in key:
            return url
    return ""

def clean_desc(desc):
    """清理描述中的来源标记和多余空格"""
    if not desc: return ""
    desc = desc.replace("（来源）", "")
    desc = desc.replace("（API 来源）", "")
    desc = desc.replace("（来源待确认）", "")
    desc = desc.replace("（来源待确认，日期待确认）", "")
    desc = desc.replace("（来源）", "。")
    import re
    desc = re.sub(r'\s+', ' ', desc).strip()
    desc = desc.strip("。，,;.;，")
    return desc[:200]

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    with open(DST, 'r', encoding='utf-8') as f:
        ref = json.load(f)

    # 合并 logo 映射
    for m in ref:
        if m.get("org") and m.get("logoUrl"):
            EXTRA_LOGOS[m["org"].lower()] = m["logoUrl"]

    converted = []
    for m in raw["models"]:
        date = m.get("date_str", "")
        if not date and m.get("year"):
            date = str(m["year"])
            if m.get("month"): date += "-" + str(m["month"]).zfill(2)
            if m.get("day"): date += "-" + str(m["day"]).zfill(2)

        # 没有具体日期的只显示年月
        display_date = date
        if date and date.endswith("-01") and not m.get("day"):
            display_date = date[:7]

        desc = clean_desc(m.get("description") or "")

        converted.append({
            "name": m["name"],
            "org": m.get("company", ""),
            "logoUrl": get_logo(m.get("company", "")),
            "date": display_date,
            "repo": "",
            "tags": ["Featured"] if m.get("highlight") else [],
            "description": {"zh-CN": desc, "en": desc}
        })

    converted.sort(key=lambda x: x["date"], reverse=True)

    with open(DST, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"转换完成: {len(converted)} 条")
    print(f"年代范围: {converted[-1]['date']} ~ {converted[0]['date']}")
    print(f"公司数: {len(set(m['org'] for m in converted if m['org']))}")

if __name__ == "__main__":
    main()