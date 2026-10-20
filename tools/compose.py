#!/usr/bin/env python3
"""Deterministic paper selection from a tagged mathematics question bank."""
from __future__ import annotations
import argparse
import random
import re
from pathlib import Path
import yaml
try:
    from .validate import validate
except ImportError:
    from validate import validate

ROOT = Path(__file__).resolve().parents[1]


def select_questions(*, topic=None, method=None, archetype=None, level=None, kind=None,
                     min_difficulty=1, max_difficulty=5, count=10, seed=2026, include_worked=False):
    errors, _ = validate()
    if errors:
        raise ValueError('invalid question bank: '+ '; '.join(errors))
    if not (1 <= min_difficulty <= max_difficulty <= 5) or count < 1:
        raise ValueError('invalid difficulty range or count')
    primary = yaml.safe_load((ROOT/'config/monotonicity.yml').read_text(encoding='utf8'))
    allowed = set(primary['question_ids'] + (primary['worked_ids'] if include_worked else []))
    available=[]
    for qid in sorted(allowed):
        meta=yaml.safe_load((ROOT/'questions'/qid/'metadata.yml').read_text(encoding='utf8'))
        if not (min_difficulty <= meta['difficulty'] <= max_difficulty): continue
        if topic and topic not in meta.get('topics', []) and topic not in meta.get('topic_ids', []): continue
        if method and method not in meta.get('methods', []) and method not in meta.get('method_ids', []):continue
        if archetype and archetype not in meta.get('archetypes',[]):continue
        if level and level != meta.get('level'):continue
        if kind and kind != meta.get('type'):continue
        available.append(qid)
    if len(available)<count:
        raise ValueError(f'only {len(available)} questions match; requested {count}; adjust filters')
    rng = random.Random(seed)
    return rng.sample(available,count)


def main():
    p=argparse.ArgumentParser(description='Write deterministic YAML for standalone workbook or answer key')
    p.add_argument('--topic',help='Legacy knowledge ID, e.g. K-FUN-MONO')
    p.add_argument('--method',help='Legacy method ID, e.g. M-DERIV-SIGN')
    p.add_argument('--archetype',help='e.g. A-FUN-04')
    p.add_argument('--level',choices=['foundation','intermediate','advanced','competition'])
    p.add_argument('--type',dest='kind',choices=['choice','fill','proof','solution'])
    p.add_argument('--min-difficulty',type=int,default=1)
    p.add_argument('--max-difficulty',type=int,default=5)
    p.add_argument('--count',type=int,default=10)
    p.add_argument('--seed',type=int,default=2026)
    p.add_argument('--include-worked',action='store_true')
    p.add_argument('--slug',default='custom_paper')
    p.add_argument('--out',default='config/custom_paper.yml')
    args=p.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9_-]{1,48}',args.slug):
        p.error('slug must be ASCII [a-z][a-z0-9_-]*')
    path=(ROOT/args.out).resolve()
    if not path.is_relative_to(ROOT/'config') or path.suffix not in ('.yml','.yaml'):
        p.error('output must be a YAML file under config/')
    try:
        chosen=select_questions(topic=args.topic, method=args.method, archetype=args.archetype,
            level=args.level,kind=args.kind,min_difficulty=args.min_difficulty,
            max_difficulty=args.max_difficulty,count=args.count,seed=args.seed,include_worked=args.include_worked)
    except ValueError as exc:
        p.error(str(exc))
    path.parent.mkdir(parents=True,exist_ok=True)
    content={'title':'自动组卷练习','slug':args.slug,'chapter':'函数与导数',
             'worked_ids':[],'question_ids':chosen}
    path.write_text(yaml.safe_dump(content,allow_unicode=True,sort_keys=False),encoding='utf8')
    print('Created:',path.relative_to(ROOT),'; IDs:',', '.join(chosen))

if __name__=='__main__':main()
