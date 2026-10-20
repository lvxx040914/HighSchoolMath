#!/usr/bin/env python3
"""V1.4 editorial precheck ledger: completeness, staleness and canonical links.

This only checks the integrity of AI-assisted PRELIMINARY notes.
It never grants independent human math approval or publishing rights.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = ('metadata.yml', 'stem.tex', 'solution.tex', 'answer.tex')
EQUIV = {'same_problem', 'algebraic_equivalent', 'substitution_equivalent'}
RELATIONS = EQUIV | {'structural_variant', 'interval_variant', 'shifted_objective',
                      'domain_restriction', 'related_parameter_family', 'different_task_same_function'}


def validate_review(root=ROOT, *, data=None):
    root = Path(root)
    errors=[]
    ledger = root / 'review/v1_4_audit.yml'
    if data is None:
        try:
            data=yaml.safe_load(ledger.read_text(encoding='utf8'))
        except (OSError, yaml.YAMLError) as exc:
            return [f'audit ledger not readable: {exc}'], 0
    if not isinstance(data,dict):
        return ['audit ledger must be a mapping'],0
    items=data.get('entries',[])
    if not isinstance(items,list):
        return ['audit entries must be a list'],0
    known={d.name for d in (root/'questions').iterdir() if d.is_dir()}
    seen=set()
    for item in items:
        if not isinstance(item,dict):
            errors.append('audit item must be a mapping');continue
        qid=item.get('id')
        if not isinstance(qid,str):
            errors.append('audit item missing ID');continue
        if qid in seen:
            errors.append(f'{qid}: duplicate audit entry')
        seen.add(qid)
        if qid not in known:
            errors.append(f'{qid}: nonexistent question');continue
        folder=root/'questions'/qid
        try:
            meta=yaml.safe_load((folder/'metadata.yml').read_text(encoding='utf8'))
        except (OSError,yaml.YAMLError) as exc:
            errors.append(f'{qid}: unreadable metadata: {exc}');continue
        if meta.get('review_status') != 'draft':
            errors.append(f'{qid}: preliminary audit cannot promote draft review_status')
        if item.get('result')!='precheck_consistent' or item.get('human_review_required') is not True:
            errors.append(f'{qid}: preliminary-only review flags missing')
        for key in ('proof_check','boundary_check'):
            if not isinstance(item.get(key),str) or len(item[key]) < 8:
                errors.append(f'{qid}: missing detailed {key}')
        if item.get('source_review')!='not_independently_verified':
            errors.append(f'{qid}: copyright/source check must remain pending')
        if item.get('difficulty_after')!=meta.get('difficulty'):
            errors.append(f'{qid}: difficulty audit differs from metadata')
        digests=item.get('content_sha256',{})
        if not isinstance(digests,dict) or set(digests)!=set(FILES):
            errors.append(f'{qid}: incorrect digest file list');continue
        for filename in FILES:
            file=folder/filename
            if not file.is_file() or digests[filename]!=hashlib.sha256(file.read_bytes()).hexdigest():
                errors.append(f'{qid}: stale audit due to {filename} content change')
        relation=meta.get('review_relation')
        audit_relation=item.get('relation')
        if relation != audit_relation:
            errors.append(f'{qid}: relation metadata and audit differ')
        if relation is not None:
            target=relation.get('target') if isinstance(relation,dict) else None
            kind=relation.get('kind') if isinstance(relation,dict) else None
            if not isinstance(target,str) or target not in known or target==qid or kind not in RELATIONS:
                errors.append(f'{qid}: invalid relation target or kind')
    if seen != known:
        errors.append(f'audit coverage mismatch: missing={sorted(known-seen)}, extraneous={sorted(seen-known)}')
    groups=data.get('canonical_equivalence_groups')
    if not isinstance(groups,list):
        errors.append('missing canonical equivalence groups');groups=[]
    grouped=set()
    for group in groups:
        if not isinstance(group,dict):
            errors.append('invalid canonical group');continue
        members=group.get('members',[])
        canonical=group.get('canonical')
        if not isinstance(members,list) or len(members)<2 or len(set(members))!=len(members) or canonical not in members:
            errors.append(f'bad canonical group {canonical}');continue
        for qid in members:
            if qid in grouped or qid not in known:
                errors.append(f'{qid}: repeated/unknown equivalence member')
            grouped.add(qid)
            if qid!=canonical and qid in known:
                meta=yaml.safe_load((root/'questions'/qid/'metadata.yml').read_text(encoding='utf8'))
                rel=meta.get('review_relation',{})
                if rel.get('target')!=canonical or rel.get('kind') not in EQUIV:
                    errors.append(f'{qid}: equivalence group inconsistent with its relation')
    return errors,len(seen)


def main():
    errors,n=validate_review()
    if errors:
        for error in errors:print('ERROR:',error)
        raise SystemExit(1)
    print(f'PASS: preliminary review coverage {n}/40; source hashes, duplicate relations, draft-only gates checked.')

if __name__=='__main__':main()
