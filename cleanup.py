#!/usr/bin/env python3
"""清理 models.json 中的脏数据"""
import json, re

SRC = "D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布/models.json"
DST = "D:/WebDesign/ai-model-history/docs/models.json"

# 脏公司名 → 正确公司名映射
COMPANY_FIX = {
    "**OpenAI**": "OpenAI",
    "**DeepSeek V4 Pro**": "DeepSeek",
    "01.AI（李开复）": "01.AI",
    "Google/CMU": "Google",
    "OpenAI / Google": "OpenAI",
    "OpenAI/Anthropic/Mistral": "OpenAI",
    "H轮650亿美元": "",
    "**超500亿**融资": "",
    "**160亿港元**组合融资": "",
    "**314亿港元**配股": "",
    "**1.6T**": "",
    "**1.6T（激活49B）**": "",
    "**1M**": "",
    "**2.4T**": "",
    "**2.7T**": "",
    "**2.8T**": "",
    "**2T**": "",
    "**Apache 2.0**": "",
    "**~1T**": "",
    "**✅ MIT**": "",
    "-": "",
    "—": "",
    "4/24": "",
    "81.2%": "",
    "~$1/$3（估算）": "",
    "华盛顿大学/Allen AI": "Allen AI",
    "微软/NVIDIA": "微软",
    "微软/威斯康星大学": "微软",
    "智谱AI / MiniMax": "智谱AI",
    "阿里/达摩院": "阿里",
}

def strip_markdown(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # [text](url)
    text = re.sub(r'⚠️', '', text)  # warning emoji
    text = re.sub(r'🌟', '', text)  # star
    text = re.sub(r'##?\s*', '', text)  # headings
    text = re.sub(r'---', '', text)  # horizontal rules
    text = re.sub(r'>\s*', '', text)  # blockquotes
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    models = raw['models']
    total = len(models)
    fixed_company = 0
    fixed_desc = 0
    removed = 0

    cleaned = []
    for m in models:
        # 修复公司名
        company = m.get('company', '')
        if company in COMPANY_FIX:
            new_company = COMPANY_FIX[company]
            if not new_company:
                removed += 1
                continue  # 跳过无意义的条目
            m['company'] = new_company
            fixed_company += 1
        elif company.startswith('**') or company.startswith('*'):
            removed += 1
            continue  # 跳过所有以**开头的脏数据

        # 清理描述
        desc = m.get('description', '') or ''
        cleaned_desc = strip_markdown(desc)
        if cleaned_desc != desc:
            m['description'] = cleaned_desc
            fixed_desc += 1

        # 修复日期格式
        date_str = m.get('date_str', '')
        if date_str and len(date_str) == 7:  # YYYY-MM
            m['date_str'] = date_str + '-01'

        cleaned.append(m)

    # 更新原始文件
    raw['models'] = cleaned
    raw['total'] = len(cleaned)
    raw['companies'] = sorted(set(m['company'] for m in cleaned if m['company']))

    with open(SRC, 'w', encoding='utf-8') as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

    print(f"原始: {total} 条")
    print(f"清理后: {len(cleaned)} 条")
    print(f"移除脏数据: {removed} 条")
    print(f"修复公司名: {fixed_company} 条")
    print(f"清理描述: {fixed_desc} 条")
    print(f"公司数: {len(raw['companies'])} 个")

if __name__ == '__main__':
    main()