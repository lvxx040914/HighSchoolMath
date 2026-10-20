#!/usr/bin/env python3
"""Generate the question index and build student/teacher PDFs from one bank."""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
import yaml
from validate import validate

ROOT = Path(__file__).resolve().parents[1]


def generate():
    errors, count = validate()
    if errors:
        sys.stderr.write('\n'.join(f'ERROR: {e}' for e in errors) + '\n')
        raise SystemExit(1)
    topic = yaml.safe_load((ROOT/'config/monotonicity.yml').read_text(encoding='utf-8'))
    ids = topic['question_ids']
    out = ROOT/'tex/generated'
    out.mkdir(exist_ok=True, parents=True)
    (out/'questions.tex').write_text('% AUTO-GENERATED; edit config/monotonicity.yml instead.\n' + '\n'.join(r'\showquestion{' + qid + '}' for qid in ids) + '\n',encoding='utf-8')
    (out/'solutions.tex').write_text('% AUTO-GENERATED; edit config/monotonicity.yml instead.\n' + '\n'.join(r'\showanswer{' + qid + '}' for qid in ids) + '\n',encoding='utf-8')
    print(f'Generated indexes: {len(ids)} questions ({count} available).')


def build(edition):
    if not shutil.which('latexmk') or not shutil.which('xelatex'):
        sys.stderr.write('ERROR: latexmk and xelatex are required for PDF build.\n')
        raise SystemExit(2)
    dist = ROOT/'dist'
    dist.mkdir(exist_ok=True)
    cmd = ['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error',f'-outdir={dist}','-quiet',f'tex/{edition}.tex']
    print('Building:', edition, flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True)
    pdf = dist/f'{edition}.pdf'
    target = dist/f'monotonicity_{edition}.pdf'
    shutil.copyfile(pdf,target)
    print('Created:', target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edition',choices=['student','teacher','all'],default='all')
    parser.add_argument('--generate-only',action='store_true')
    args = parser.parse_args()
    generate()
    if not args.generate_only:
        for edition in (['student','teacher'] if args.edition == 'all' else [args.edition]):
            build(edition)

if __name__ == '__main__':
    main()
