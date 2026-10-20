#!/usr/bin/env python3
"""Create human-readable atlas from canonical YAML catalogs; --check detects drift."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def render():
    know=yaml.safe_load((ROOT/'catalog/knowledge_map.yml').read_text(encoding='utf-8'))
    methods=yaml.safe_load((ROOT/'catalog/methods.yml').read_text(encoding='utf-8'))
    archetypes=yaml.safe_load((ROOT/'catalog/archetypes.yml').read_text(encoding='utf-8'))
    tracks={'core':'主线候选','selective':'选必候选','cross':'跨章节综合','extension':'竞赛拓展'}
    lines=['# 高中数学知识地图｜V1.1','',
           '> 从 `catalog/knowledge_map.yml` 自动生成。此目录是项目的教学编辑结构，**不是课程标准原文章节的复制**；主线与选必归属尚需逐项复核。','',
           '官方参考：<https://www.ictr.edu.cn/download_center/put.html> （普通高中数学课程标准，2017 年版 2020 年修订）。','',
           '分层标记：主线候选 / 选必候选 / 跨章节综合 / 竞赛拓展。`T-*` 为稳定主题编号；编辑状态 `planned` 表示计划覆盖，不代表已有对应讲义。','']
    for d in know['domains']:
        lines+=['## '+d['id']+'｜'+d['title'],'','| ID | 知识主题 | 编辑分层 | 前置主题 |','|---|---|---|---|']
        for t in d['topics']:
            lines.append(f"| `{t['id']}` | {t['title']} | {tracks[t['track']]} | {', '.join('`'+r+'`' for r in t['prerequisites']) or '—'} |")
        lines.append('')
    methodlines=['# 解题方法与典型题型目录｜V1.1','',
                 '> 以下目录由 `catalog/methods.yml` 与 `catalog/archetypes.yml` 自动生成，所有条目均为待逐步编写的编辑规划，不代表已经完成。','',
                 '## 解题方法库','','| 方法 ID | 方法名称 | 适用条件 / 检查要点 | 典型失误 |', '|---|---|---|---|']
    for m in methods['methods']:
        methodlines.append(f"| `{m['id']}` | {m['title']} | {m['conditions']} | {m['failure_mode']} |")
    methodlines+=['','## 典型题型与变式轴','','| 题型 ID | 题型名称 | 对应方法 | 两种典型变式 |', '|---|---|---|---|']
    for a in archetypes['archetypes']:
        methodlines.append(f"| `{a['id']}` | {a['title']} | {', '.join('`'+m+'`' for m in a['methods'])} | {'；'.join(a['variant_axes'])} |")
    methodlines+=['','### 使用约束','','- 方法不能仅列步骤，还要提供数学原理、严格适用条件、失败情形和反例。','- 每类题型要明确母题、可审计的典型变式和不可逆变形；不能用改数字制造虚假题量。','- 每题的 `archetypes` 字段指向这里的题型 ID，`topics` / `methods` 继续使用 V1.0 实体 ID；将来迁移需要显式脚本。','']
    return {'docs/KNOWLEDGE_ATLAS.md':'\n'.join(lines).rstrip('\n')+'\n','docs/METHOD_AND_ARCHETYPE_ATLAS.md':'\n'.join(methodlines).rstrip('\n')+'\n'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    expected=render();bad=[]
    for path,data in expected.items():
        target=ROOT/path
        if a.check:
            if not target.exists() or target.read_text(encoding='utf-8')!=data:bad.append(path)
        else:target.write_text(data,encoding='utf-8')
    if bad:raise SystemExit('Catalog docs out of date: '+', '.join(bad)+'; run python tools/render_catalog.py')
    print(('PASS: catalog docs match YAML' if a.check else 'Generated: '+', '.join(expected)))
if __name__=='__main__':main()
