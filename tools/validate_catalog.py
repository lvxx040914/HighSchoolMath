#!/usr/bin/env python3
"""Validate the V1.1 taxonomy and cross-links without modifying V1.0 content."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
TOPIC_RE = re.compile(r'^T-[A-Z]{3}-\d{2}$')
METHOD_RE = re.compile(r'^MT-[A-Z0-9]+(?:-[A-Z0-9]+)*$')
ARCHETYPE_RE = re.compile(r'^A-[A-Z]{3}-\d{2}$')
TRACKS = {'core','selective','cross','extension'}


def _load(path, errors):
    try:
        obj = yaml.safe_load(path.read_text(encoding='utf-8'))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f'{path.name}: cannot load: {exc}')
        return {}
    if not isinstance(obj,dict) or obj.get('schema_version') != SCHEMA_VERSION:
        errors.append(f'{path.name}: expected schema_version 1 object')
        return {}
    return obj


def _required_text(item, attr, ctx, errors):
    value=item.get(attr)
    if not isinstance(value,str) or not value.strip():
        errors.append(f'{ctx}: missing {attr}')


def _required_list(item, attr, ctx, errors, minimum=0):
    value=item.get(attr)
    if not isinstance(value,list) or len(value)<minimum or any(not isinstance(v,str) or not v.strip() for v in value):
        errors.append(f'{ctx}: invalid {attr}')
        return []
    if len(value)!=len(set(value)):
        errors.append(f'{ctx}: duplicate entries in {attr}')
    return value


def _cycle_check(adjacency,errors):
    color={}
    def visit(node,stack):
        if color.get(node)==1:
            errors.append('prerequisite cycle: '+' -> '.join(stack+[node]));return
        if color.get(node)==2:return
        color[node]=1
        for pred in adjacency.get(node,[]):
            if pred in adjacency:visit(pred,stack+[node])
        color[node]=2
    for node in adjacency:visit(node,[])


def validate_catalog(root=ROOT):
    root=Path(root)
    errors=[]
    knowledge=_load(root/'catalog/knowledge_map.yml',errors)
    methods_doc=_load(root/'catalog/methods.yml',errors)
    archetypes_doc=_load(root/'catalog/archetypes.yml',errors)
    topics={}
    families=set()
    for d in knowledge.get('domains',[]):
        if not isinstance(d,dict):errors.append('domains: invalid element');continue
        did=d.get('id');_required_text(d,'title',did,errors)
        if not isinstance(did,str) or not re.fullmatch(r'D-[A-Z]{3}',did) or did in families:
            errors.append(f'domain id invalid/duplicate: {did!r}')
        families.add(did)
        if not isinstance(d.get('topics'),list) or not d['topics']:
            errors.append(f'{did}: empty topics');continue
        for t in d['topics']:
            if not isinstance(t,dict):errors.append(f'{did}: invalid topic element');continue
            tid=t.get('id')
            if not isinstance(tid,str) or not TOPIC_RE.fullmatch(tid) or not tid.startswith(f'T-{did[2:]}-') or tid in topics:
                errors.append(f'topic invalid/duplicate: {tid!r}')
            _required_text(t,'title',tid,errors)
            if t.get('track') not in TRACKS:errors.append(f'{tid}: invalid track')
            _required_list(t,'prerequisites',tid,errors)
            _required_list(t,'legacy_knowledge_ids',tid,errors) if 'legacy_knowledge_ids' in t else None
            topics[tid]=t
    adjacency={tid:t.get('prerequisites',[]) for tid,t in topics.items()}
    for tid,req in adjacency.items():
        for x in req if isinstance(req,list) else []:
            if x not in topics:errors.append(f'{tid}: unknown prerequisite {x}')
            if x==tid:errors.append(f'{tid}: self-dependency')
    _cycle_check(adjacency,errors)

    methods={}
    for m in methods_doc.get('methods',[]):
        if not isinstance(m,dict):errors.append('methods: invalid entry');continue
        mid=m.get('id')
        if not isinstance(mid,str) or not METHOD_RE.fullmatch(mid) or mid in methods:
            errors.append(f'method invalid/duplicate: {mid!r}')
        for key in ('title','conditions','failure_mode'):_required_text(m,key,mid,errors)
        for tid in _required_list(m,'related_topics',mid,errors,minimum=1):
            if tid not in topics:errors.append(f'{mid}: unknown topic {tid}')
        methods[mid]=m

    archetypes={}
    for a in archetypes_doc.get('archetypes',[]):
        if not isinstance(a,dict):errors.append('archetypes: invalid entry');continue
        aid=a.get('id')
        if not isinstance(aid,str) or not ARCHETYPE_RE.fullmatch(aid) or aid in archetypes:
            errors.append(f'archetype invalid/duplicate: {aid!r}')
        for key in ('title','pitfall'):_required_text(a,key,aid,errors)
        for tid in _required_list(a,'topics',aid,errors,minimum=1):
            if tid not in topics:errors.append(f'{aid}: unknown topic {tid}')
        for mid in _required_list(a,'methods',aid,errors,minimum=1):
            if mid not in methods:errors.append(f'{aid}: unknown method {mid}')
        _required_list(a,'variant_axes',aid,errors,minimum=2)
        archetypes[aid]=a

    for dirname,kind,attr in [('knowledge','legacy knowledge','legacy_knowledge_ids'),('methods','legacy method','legacy_method_id')]:
        legacy_files=list((root/dirname).glob('*.yml'))
        if not legacy_files:errors.append(f'{dirname}: missing V1.0 entities')
        linked=[]
        entries=topics.values() if dirname=='knowledge' else methods.values()
        for e in entries:
            val=e.get(attr,[] if dirname=='knowledge' else None)
            linked.extend(val if isinstance(val,list) else [val] if isinstance(val,str) else [])
        for key,count in Counter(linked).items():
            if count!=1:errors.append(f'{kind} alias duplicated: {key}')
        known={p.stem for p in legacy_files}
        for key in linked:
            if key not in known:errors.append(f'{kind} alias not found: {key}')
        for key in sorted(known-set(linked)):
            errors.append(f'{kind} missing catalog alias: {key}')

    question_count=0
    for folder in (root/'questions').glob('HSM-*/'):
        f=folder/'metadata.yml'
        if not f.is_file():continue
        try:meta=yaml.safe_load(f.read_text(encoding='utf-8'))
        except (OSError,yaml.YAMLError) as exc:
            errors.append(f'{folder.name}: cannot read metadata: {exc}');continue
        if not isinstance(meta,dict):errors.append(f'{folder.name}: invalid metadata');continue
        if 'archetypes' in meta:
            question_count+=1
            for aid in _required_list(meta,'archetypes',folder.name,errors,minimum=1):
                if aid not in archetypes:errors.append(f'{folder.name}: unknown archetype {aid}')
    return errors,{'domains':len(families),'topics':len(topics),'methods':len(methods),
                   'archetypes':len(archetypes),'mapped_questions':question_count}


def main():
    errors,counts=validate_catalog()
    if errors:
        for e in errors:print('ERROR:',e,file=sys.stderr)
        raise SystemExit(1)
    print('PASS: catalog cross-links and legacy aliases valid: '+', '.join(f'{k}={v}' for k,v in counts.items()))

if __name__=='__main__':main()
