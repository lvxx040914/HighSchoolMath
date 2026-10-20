PYTHON ?= python3
.PHONY: review validate catalog check report test generate student lecture workbook teacher answer_key build pdfcheck clean

validate:
	$(PYTHON) tools/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v

generate:
	$(PYTHON) tools/build.py --generate-only

student lecture workbook teacher answer_key:
	$(PYTHON) tools/build.py --edition $@

build:
	$(PYTHON) tools/build.py --edition all

clean:
	latexmk -C -outdir=dist -jobname=monotonicity_lecture tex/student.tex
	latexmk -C -outdir=dist -jobname=monotonicity_workbook tex/workbook.tex
	latexmk -C -outdir=dist -jobname=monotonicity_teacher tex/teacher.tex
	latexmk -C -outdir=dist -jobname=monotonicity_answer_key tex/answer_key.tex

catalog:
	$(PYTHON) tools/render_catalog.py

report:
	$(PYTHON) tools/report_catalog.py

review:
	$(PYTHON) tools/validate_review.py

check:
	$(PYTHON) tools/validate.py
	$(PYTHON) tools/validate_review.py
	$(PYTHON) tools/report_review.py --check
	$(PYTHON) tools/validate_catalog.py
	$(PYTHON) tools/render_catalog.py --check
	$(PYTHON) -m unittest discover -s tests -v

pdfcheck:
	$(PYTHON) tools/verify_pdf.py
