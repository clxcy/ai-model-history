#!/usr/bin/env python3
"""
重新解析 markdown 文件，从 section header 提取具体日期。
"""
import os, re, json, glob

SRC_DIR = "D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布"
DST = "D:/WebDesign/my-obs/my-obs/1.公众号运营/文章/选题资料/大模型发布/models.json"

def parse_md(filepath):
    """从 markdown 文件提取模型数据"""
    models = []
    basename = os.path.basename(filepath)
    m = re.match(r"(\d{4})年(\d{1,2})月", basename)
    if not m: return models
    year, month = int(m.group(1)), int(m.group(2))

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_day = None
    in_table = False
    headers = []

    for line in lines:
        # 检查 section header（如 "### 7月1日"、"### 7月2日"）
        header_match = re.match(r"###+\s*(\d{1,2})月(\d{1,2})?日?", line)
        if header_match:
            m_month = int(header_match.group(1))
            m_day = header_match.group(2)
            if m_month == month:  # 只匹配当前月份
                current_day = int(m_day) if m_day else None
            in_table = False
            continue

        # 检查表格行
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not cells:
                continue

            # 判断是否是表头
            if all(c.startswith(":") or c == "---" for c in cells if c):
                in_table = True
                continue
            if not in_table:
                continue
            if len(cells) < 3:
                continue

            # 第一列可能是日期列或模型名列
            col0 = cells[0]
            table_day = None

            # 尝试从第一列提取日期（如 "4/6"、"4月"）
            date_match = re.match(r"(\d{1,2})/(\d{1,2})", col0)
            if date_match:
                table_day = int(date_match.group(2))
            else:
                date_match2 = re.match(r"(\d{1,2})月", col0)
                if date_match2:
                    d = int(date_match2.group(1))
                    if d <= 31:  # 是日期不是月份
                        table_day = d

            if len(cells) == 4:
                # 四列格式：日期 | 模型 | 公司 | 信息
                model_name = cells[1]
                company = cells[2]
                info = cells[3]
                if cells[0] and not date_match and not date_match2:
                    # 第一列可能是模型名（无日期列格式）
                    model_name = cells[0]
                    company = cells[1]
                    info = cells[2]
            elif len(cells) == 3:
                model_name = cells[0]
                company = cells[1]
                info = cells[2]
            else:
                continue

            # 跳过表头和无意义行
            if model_name in ["模型", "事件", "模型", "---"]:
                continue
            if not model_name:
                continue

            # 确定最终日期
            day = table_day or current_day
            date_str = f"{year}-{month:02d}"
            if day:
                date_str += f"-{day:02d}"

            is_starred = "🌟" in model_name
            model_name = model_name.replace("🌟", "").strip()

            # 提取链接
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", info)
            sources = [{"label": l[0], "url": l[1]} for l in links]

            models.append({
                "name": model_name,
                "company": company,
                "params": "",
                "params_detail": "",
                "description": info,
                "open_source": "开源" in info,
                "highlight": is_starred,
                "year": year,
                "month": month,
                "day": day,
                "date_str": date_str,
                "source": sources
            })

    return models

def main():
    all_models = []
    pattern = os.path.join(SRC_DIR, "*大模型发布汇总*.md")
    files = sorted(glob.glob(pattern))
    print(f"找到 {len(files)} 个文件")

    for filepath in files:
        models = parse_md(filepath)
        print(f"  {os.path.basename(filepath)}: {len(models)} 条")
        all_models.extend(models)

    # 去重
    seen = set()
    unique = []
    for m in all_models:
        key = (m["name"], m["company"], m["date_str"])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    print(f"\n总计: {len(all_models)} → 去重后 {len(unique)} 条")
    print(f"有具体日期: {sum(1 for m in unique if m['day'])} 条")
    print(f"公司数: {len(set(m['company'] for m in unique if m['company']))}")

    output = {
        "total": len(unique),
        "generated_at": "2026-07-23",
        "companies": sorted(set(m["company"] for m in unique if m["company"])),
        "models": unique
    }

    with open(DST, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"已保存: {DST}")

if __name__ == "__main__":
    main()