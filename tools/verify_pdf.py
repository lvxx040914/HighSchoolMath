#!/usr/bin/env python3
"""Verify four generated PDF products and solution leakage boundaries."""
from pathlib import Path
import re
import shutil
import subprocess
import yaml

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'

def main():
    if not shutil.which('pdftotext'):
        raise SystemExit('pdftotext required; install poppler (brew install poppler)')
    cfg=yaml.safe_load((ROOT/'config/monotonicity.yml').read_text(encoding='utf8'))
    n=len(cfg['question_ids'])
    bodies={}
    for edition in ('lecture','workbook','teacher','answer_key'):
        f=DIST/f'monotonicity_{edition}.pdf'
        if not f.exists() or f.stat().st_size<10000:
            raise SystemExit(f'missing/small PDF: {f}')
        bodies[edition]=subprocess.check_output(['pdftotext','-layout',str(f),'-'],text=True)
    lecture,workbook,teacher,key=(bodies[x] for x in ('lecture','workbook','teacher','answer_key'))
    if '专题训练答案与解析' in lecture or '专题训练答案与解析' in workbook:
        raise SystemExit('student-facing PDF leaked training solution section')
    if '专题训练答案与解析' not in teacher:
        raise SystemExit('teacher edition missing solution section')
    if '答案速查册' not in key or '专项习题册' not in workbook:
        raise SystemExit('standalone documents have incorrect title')
    if '规范解答' in workbook or '规范解答' in key:
        raise SystemExit('workbook or answer key contains worked proof')
    for i,qid in enumerate(cfg['question_ids'],start=1):
        if qid not in workbook or qid not in key or qid not in teacher:
            raise SystemExit(f'training ID omitted from a PDF: {qid}')
        if not re.search(rf'第\s*{i}\s*题',workbook):
            raise SystemExit(f'workbook number {i} missing')
    for qid in cfg['worked_ids']:
        if qid not in lecture or qid not in teacher:
            raise SystemExit(f'worked ID {qid} missing')
    if cfg['worked_ids'][0] in workbook or cfg['worked_ids'][0] in key:
        raise SystemExit('standalone collection leaked worked example')
    print(f'PASS: 4 PDF products, {n} consistent training IDs, {len(cfg["worked_ids"])} worked examples; no answer leakage')

if __name__=='__main__':main()
