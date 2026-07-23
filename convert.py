#!/usr/bin/env python3
import json

with open("D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布/models.json", "r", encoding="utf-8") as f:
    our = json.load(f)

with open("D:/WebDesign/ai-model-history/docs/models.json", "r", encoding="utf-8") as f:
    ref = json.load(f)

org_logos = {}
for m in ref:
    if m.get("org") and m.get("logoUrl"):
        org_logos[m["org"].lower()] = m["logoUrl"]

extra_logos = {
    "openai": "https://github.com/openai.png",
    "google": "https://github.com/google.png",
    "google deepmind": "https://github.com/google-deepmind.png",
    "anthropic": "https://github.com/anthropics.png",
    "meta": "https://github.com/facebook.png",
    "deepseek": "https://github.com/deepseek-ai.png",
    "mistral": "https://github.com/mistralai.png",
    "cohere": "https://github.com/cohere-ai.png",
    "microsoft": "https://github.com/microsoft.png",
    "nvidia": "https://github.com/nvidia.png",
    "阿里/千问": "https://github.com/alibaba.png",
    "百度": "https://github.com/baidu.png",
    "腾讯": "https://github.com/tencent.png",
    "字节跳动": "https://github.com/bytedance.png",
    "智谱AI": "https://github.com/zhipuai.png",
    "月之暗面": "https://github.com/moonshotai.png",
    "minimax": "https://github.com/MiniMax-AI.png",
    "xai": "https://github.com/xai-org.png",
    "stability ai": "https://github.com/Stability-AI.png",
}

def get_logo(company):
    if not company:
        return ""
    c = company.lower().strip()
    for key, url in {**org_logos, **extra_logos}.items():
        if key in c or c in key:
            return url
    return ""

converted = []
for m in our["models"]:
    date = m.get("date_str", "")
    if not date and m.get("year"):
        date = str(m["year"])
        if m.get("month"):
            date += "-" + str(m["month"]).zfill(2)
        if m.get("day"):
            date += "-" + str(m["day"]).zfill(2)
    desc = (m.get("description") or "")[:200]
    converted.append({
        "name": m["name"],
        "org": m.get("company", ""),
        "logoUrl": get_logo(m.get("company", "")),
        "date": date,
        "repo": "",
        "tags": ["Featured"] if m.get("highlight") else [],
        "description": {"zh-CN": desc, "en": desc}
    })

converted.sort(key=lambda x: x["date"], reverse=True)

with open("D:/WebDesign/ai-model-history/docs/models.json", "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)

print(f"转换完成: {len(converted)} 条")
first = converted[-1]["date"]
last = converted[0]["date"]
print(f"年代范围: {first} ~ {last}")
companies = len(set(m["org"] for m in converted if m["org"]))
print(f"公司数: {companies}")