#!/usr/bin/env python3
"""Smoke-check compiled student/teacher PDFs with pdftotext (Poppler)."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


def main():
    if not shutil.which('pdftotext'):
        raise SystemExit('pdftotext is required (poppler-utils)')
    texts = {}
    for edition in ('student', 'teacher'):
        pdf = DIST / f'monotonicity_{edition}.pdf'
        if not pdf.is_file() or pdf.stat().st_size < 10_000:
            raise SystemExit(f'missing/invalid PDF: {pdf}')
        texts[edition] = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    student, teacher = texts['student'], texts['teacher']
    for edition, body in texts.items():
        for num in range(1, 31):
            if not re.search(rf'第\s*{num}\s*题', body):
                raise SystemExit(f'{edition}: training question {num} not found')
        for num in range(11, 15):
            if f'HSM-FUN-{num:04d}' not in body:
                raise SystemExit(f'{edition}: worked example {num} not found')
    if '专题训练答案与解析' in student:
        raise SystemExit('student version leaked training solutions')
    if '专题训练答案与解析' not in teacher:
        raise SystemExit('teacher version lacks solutions')
    if teacher.count('HSM-FUN-0034') < 2:
        raise SystemExit('teacher version missing final answer')
    print('PASS: student/teacher PDF smoke checks; 30 training IDs + 4 worked examples')


if __name__ == '__main__':
    main()
