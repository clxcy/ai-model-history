#!/usr/bin/env python3
"""第二轮清理：合并同公司名、删除垃圾数据"""
import json

SRC = "D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布/models.json"

# 公司名规范化映射
NORMALIZE = {
    "公司": "",
    "开源": "",
    "社区": "",
    "不确定": "",
    "市场反应": "",
    "已提交S-1申请": "",
    "金额": "",
    "参数规模": "",
    "百万上下文+极致性价比": "",
    "微信": "腾讯",
    "阿里达摩院": "阿里",
    "月之暗面（Moonshot AI）": "月之暗面",
    "智源研究院（BAAI）": "智源研究院",
    "智源研究院": "智源研究院",
    "AI2（艾伦研究所）": "AI2",
    "AI2": "AI2",
    "StepFun（阶跃星辰）": "阶跃星辰",
    "StepFun": "阶跃星辰",
    "HuggingFace": "Hugging Face",
    "Hugging Face": "Hugging Face",
    "乐天（日本）": "乐天",
    "乐天": "乐天",
    "BAIR（UC Berkeley）": "UC Berkeley",
    "UC Berkeley": "UC Berkeley",
    "Microsoft AI": "微软",
    "Facebook AI": "Meta",
    "Salesforce": "Salesforce",
    "Skywork AI": "Skywork AI",
    "Sakana AI（日本）": "Sakana AI",
    "OpenAI": "OpenAI",
    "Google DeepMind": "Google",
    "Nex AGI": "Nex AGI",
    "DeepReinforce": "DeepReinforce",
    "Stability AI": "Stability AI",
    "Nous Research": "Nous Research",
    "Black Forest Labs": "Black Forest Labs",
    "BigScience": "BigScience",
    "EleutherAI": "EleutherAI",
    "Nomic AI": "Nomic AI",
    "LM-SYS": "LM-SYS",
    "Reka AI": "Reka AI",
    "Subquadratic": "Subquadratic",
    "Zyphra": "Zyphra",
    "Apodex": "Apodex",
    "Boson AI": "Boson AI",
    "Ideogram": "Ideogram",
    "Liquid AI": "Liquid AI",
    "Thinking Machines": "Thinking Machines",
    "Mind Lab": "Mind Lab",
    "Cognition": "Cognition",
    "RWKV Foundation": "RWKV Foundation",
    "MosaicML": "MosaicML",
    "TII（阿联酋）": "TII",
    "Upstage（韩国）": "Upstage",
    "Upstage": "Upstage",
    "Yandex（俄罗斯）": "Yandex",
    "Allen AI": "Allen AI",
    "JetBrains": "JetBrains",
    "Ollama": "Ollama",
    "Midjourney": "Midjourney",
    "Runway": "Runway",
    "Bloomberg": "Bloomberg",
    "Together": "Together",
    "Snowflake": "Snowflake",
    "Databricks": "Databricks",
    "01.AI": "01.AI",
    "H Company": "H Company",
}

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    models = raw['models']
    total = len(models)
    fixed = 0
    removed = 0

    cleaned = []
    for m in models:
        company = m.get('company', '')
        if company in NORMALIZE:
            new_company = NORMALIZE[company]
            if not new_company:
                removed += 1
                continue
            m['company'] = new_company
            fixed += 1

        cleaned.append(m)

    raw['models'] = cleaned
    raw['total'] = len(cleaned)
    raw['companies'] = sorted(set(m['company'] for m in cleaned if m['company']))

    with open(SRC, 'w', encoding='utf-8') as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

    print(f"原始: {total} 条")
    print(f"清理后: {len(cleaned)} 条")
    print(f"移除: {removed} 条")
    print(f"规范化: {fixed} 条")
    print(f"公司数: {len(raw['companies'])} 个")

if __name__ == '__main__':
    main()