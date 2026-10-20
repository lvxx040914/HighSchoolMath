#!/usr/bin/env python3
"""Validate the metadata and integrity of an independent TeX question bank."""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml
try:
    from .validate_catalog import validate_catalog
except ImportError:  # python tools/validate.py
    from validate_catalog import validate_catalog

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r'^HSM-[A-Z]{3}-\d{4}$')
LEVELS = {'foundation', 'intermediate', 'advanced', 'competition'}
TYPES = {'choice', 'fill', 'proof', 'solution'}
STATUSES = {'draft', 'math_checked', 'typeset_checked', 'published'}
SOURCES = {'self_written', 'public_domain', 'licensed', 'reference_only'}


def validate():
    errors = []
    found = {}
    def ids_in(kind):
        known = set()
        for f in (ROOT/kind).glob('*.yml'):
            m = yaml.safe_load(f.read_text(encoding='utf-8'))
            if not isinstance(m, dict) or not isinstance(m.get('id'), str) or m['id'] != f.stem:
                errors.append(f'{kind}/{f.name}: invalid entity metadata')
                continue
            known.add(m['id'])
        if not known:
            errors.append(f'{kind}: empty entity collection')
        return known
    known_topics = ids_in('knowledge')
    known_methods = ids_in('methods')
    for folder in sorted((ROOT/'questions').iterdir()):
        if not folder.is_dir():
            continue
        f = folder/'metadata.yml'
        if not f.is_file():
            errors.append(f'{folder.name}: missing metadata.yml')
            continue
        try:
            meta = yaml.safe_load(f.read_text(encoding='utf-8'))
            if not isinstance(meta, dict):
                raise ValueError('metadata must be object')
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f'{folder.name}: invalid YAML: {exc}')
            continue
        qid = meta.get('id')
        if not isinstance(qid, str) or not PATTERN.fullmatch(qid) or qid != folder.name:
            errors.append(f'{folder.name}: invalid or inconsistent id {qid!r}')
        if qid in found:
            errors.append(f'{folder.name}: duplicate ID {qid}')
        found[qid] = meta
        for key in ('title', 'chapter'):
            if not isinstance(meta.get(key), str) or not meta[key].strip():
                errors.append(f'{qid}: missing {key}')
        for key in ('topics', 'methods'):
            if not isinstance(meta.get(key), list) or not meta[key] or not all(isinstance(x,str) and x.strip() for x in meta[key]):
                errors.append(f'{qid}: invalid {key}')
        for key, known in (('topics',known_topics), ('methods',known_methods)):
            for ref in meta.get(key, []) if isinstance(meta.get(key), list) else []:
                if isinstance(ref,str) and ref not in known:
                    errors.append(f'{qid}: unknown {key} reference {ref}')
        if type(meta.get('difficulty')) is not int or not (1 <= meta['difficulty'] <= 5):
            errors.append(f'{qid}: difficulty must be integer 1..5')
        for key, valid in (('level', LEVELS), ('type',TYPES), ('review_status',STATUSES)):
            if meta.get(key) not in valid:
                errors.append(f'{qid}: invalid {key}')
        source = meta.get('source')
        if not isinstance(source, dict) or source.get('kind') not in SOURCES:
            errors.append(f'{qid}: missing source / kind')
        else:
            for key in ('citation', 'permission'):
                if not isinstance(source.get(key), str) or not source[key].strip():
                    errors.append(f'{qid}: missing source.{key}')
            if source.get('kind') == 'reference_only':
                errors.append(f'{qid}: reference-only problem cannot be redistributed')
        for name in ('stem.tex','solution.tex'):
            t = folder/name
            if not t.is_file() or not t.read_text(encoding='utf-8').strip():
                errors.append(f'{qid}: missing or empty {name}')
    try:
        topic = yaml.safe_load((ROOT/'config/monotonicity.yml').read_text(encoding='utf-8'))
        ids = topic['question_ids']
        worked = topic.get('worked_ids', [])
    except (FileNotFoundError, KeyError, yaml.YAMLError) as exc:
        errors.append(f'config/monotonicity.yml: {exc}')
        ids, worked = [], []
    if not isinstance(ids, list) or not isinstance(worked, list) or not all(isinstance(v,str) for v in ids+worked):
        errors.append('question lists must contain string IDs')
    elif len(set(ids+worked)) != len(ids+worked):
        errors.append('training/worked question lists overlap or have duplicates')
    else:
        for qid in ids + worked:
            if qid not in found:
                errors.append(f'question list references missing {qid}')
    if not found:
        errors.append('question bank is empty')
    catalog_errors, _ = validate_catalog(ROOT)
    errors.extend(catalog_errors)
    return errors, len(found)


def main():
    errors, count = validate()
    if errors:
        for e in errors:
            print('ERROR:', e, file=sys.stderr)
        raise SystemExit(1)
    print(f'PASS: validated {count} questions; metadata, source and topic index complete.')

if __name__ == '__main__':
    main()
