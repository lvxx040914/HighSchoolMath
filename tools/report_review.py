#!/usr/bin/env python3
"""Render a stable audit summary from the reviewed question ledger."""
from pathlib import Path
from collections import Counter
import argparse
import yaml
try:
    from .validate_review import ROOT, validate_review
except ImportError:
    from validate_review import ROOT, validate_review


def render(data):
    entries=data['entries']
    diff=Counter(e['difficulty_after'] for e in entries)
    out=[
        '# HighSchoolMath V1.4｜函数单调性题库质量预检报告',
        '',
        '> 本报告来自 AI 辅助数学预检，不是独立人工审稿证明；全部题目继续保持 `draft`。',
        '',
        '## 一、检查范围与结论',
        '',
        f'- 已入库：**{len(entries)}** 道；已完成逐题预检记录：**{len(entries)}** 条；独立人工审稿通过：**0** 道。',
        '- 重点检查题面条件、核心计算、参数临界值、端点、取等条件、不同根计数与答案对应关系。',
        '- 数学公式及结论的初步核查未发现必须推翻的答案；发现一处独立解析对讲义例题编号的依赖，已修订。',
        '- 基于命题等价识别出 **2 组**高重合关系：共涉及 **6 条**记录，合并数学等价命题后的独立命题约 **36 个**（未扣除一般题型相似）。',
        '- 默认 30 道训练题包含两组重复命题，按当前规则剔除数学等价记录后为 **28 个**代表题；不会在默认版本中静默删除题目。',
        '- 本次编辑难度重新标注 8 道；当前等级分布：' + '、'.join(f'{k} 级 {diff.get(k,0)} 道' for k in range(1,6)) + '。',
        '',
        '## 二、数学等价题与典型变式',
        '',
        '| 数学母题 | 相关 ID | 关系 | 建议 |',
        '|---|---|---|---|',
        '| HSM-FUN-0007 | 0014、0028、0038 | 同一道对数不等式、代数移项及代换 | 作为同一命题家族管理，组卷时避免重复 |',
        '| HSM-FUN-0006 | 0029 | 完全相同的指数切线不等式 | 默认选题优先保留母题 0006 |',
        '| HSM-FUN-0004 | 0023 | 给定区间由 `[0,+∞)` 改为 `[2,+∞)` | 属于边界变式，不是重复题 |',
        '| HSM-FUN-0002 | 0037 | 实数域问题缩到非负半轴 | 属于定义域变化，不是重复题 |',
        '| HSM-FUN-0036 | 0040 | 相同三次函数、不同目标（极值/方程根数） | 保留两个题目，促进能力迁移 |',
        '',
        '## 三、独立解析修订',
        '',
        '`HSM-FUN-0040` 的 V1.3 解答仅写“由例题 2 可知”，这不适用于单题抽取。V1.4 直接从',
        r"$F'(x)=3(x+1)(x-1)$ 推导单调区间、极值 $2$ 与 $-2$，并独立说明 $t=\pm2$ 的切触点只计一个不同实根。",
        '',
        '## 四、难度重新标定（编辑建议，不是统计标定）',
        '',
        '| ID | V1.3 | V1.4 | 理由 |',
        '|---|---:|---:|---|',
    ]
    changes={5:4,8:4,10:5,23:3,24:4,30:4,32:4,33:5}
    for n,old in changes.items():
        item=entries[n-1]
        out.append(f"| {item['id']} | {old} | {item['difficulty_after']} | {item['difficulty_calibration']} |")
    out+=['', '## 五、40 道题逐题检查摘要','','| 题目 ID | 关键推导复核 | 临界值／定义域检查 | 难度 |', '|---|---|---|---:|']
    for e in entries:
        out.append(f"| {e['id']} | {e['proof_check']} | {e['boundary_check']} | {e['difficulty_after']} |")
    out+=['', '## 六、发布与后续审核门槛', '',
          '1. **独立数学人工复核**：由不同于最初编写者的审阅人重新解答，并对参数条件完成正反向证明。',
          '2. **独立来源与版权审查**：目前只记录最初编写声明，不能据此认定对外素材授权完成。',
          '3. **难度实测**：当前 1–5 等级为编辑判断，并非依据学生作答数据校准。',
          '4. **重复母题编排**：保留永久 ID，但正式习题册须决定重复命题是否替换成不同数学本质的题。',
          '5. **内容变更失效**：题目的四个核心源文件任一改变，都必须更新对应审阅记录；`make check` 强制校验 SHA-256 指纹。',
          '', '## 七、复现命令','', '```bash', 'make check', 'make build', 'make pdfcheck',
          'python3 tools/compose.py --count 8 --avoid-equivalent --seed 2026', '```','']
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    errors,_=validate_review()
    if errors:raise SystemExit('review ledger invalid: '+'; '.join(errors))
    data=yaml.safe_load((ROOT/'review/v1_4_audit.yml').read_text(encoding='utf8'))
    result=render(data)
    target=ROOT/'docs/V1_4_REVIEW_REPORT.md'
    if args.check:
        if not target.exists() or target.read_text(encoding='utf8') != result:
            raise SystemExit(f'FAIL: regenerate {target} with python tools/report_review.py')
        print('PASS: audit report is synchronized with YAML ledger')
    else:
        target.write_text(result,encoding='utf8')
        print('Created:',target)

if __name__=='__main__':main()
