#!/usr/bin/env python3
"""Print honest planning and reviewed-output counts; catalog size is not completion."""
from collections import Counter
from pathlib import Path
import yaml
from validate_catalog import ROOT, validate_catalog

def main():
    errors,stat=validate_catalog()
    if errors:raise SystemExit('Catalog validation failed; run python tools/validate_catalog.py')
    statuses=Counter()
    for p in (ROOT/'questions').glob('HSM-*/metadata.yml'):
        m=yaml.safe_load(p.read_text(encoding='utf-8'))
        statuses[m.get('review_status','missing')]+=1
    print('=== HighSchoolMath V1.1 content status ===')
    print('Planned editorial index: ', ', '.join(f'{k}={v}' for k,v in stat.items()))
    print('Independent questions:   ',sum(statuses.values()))
    print('Review status:           ', ', '.join(f'{k}={v}' for k,v in sorted(statuses.items())))
    print('Note: planned topics/methods/archetypes are not completed teaching units.')
if __name__=='__main__':main()
