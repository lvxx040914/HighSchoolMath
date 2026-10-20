PYTHON ?= python3
.PHONY: validate catalog check report test generate student teacher build clean

validate:
	$(PYTHON) tools/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v

generate:
	$(PYTHON) tools/build.py --generate-only

student:
	$(PYTHON) tools/build.py --edition student

teacher:
	$(PYTHON) tools/build.py --edition teacher

build:
	$(PYTHON) tools/build.py --edition all

clean:
	latexmk -C -outdir=dist tex/student.tex tex/teacher.tex

catalog:
	$(PYTHON) tools/render_catalog.py

report:
	$(PYTHON) tools/report_catalog.py

check:
	$(PYTHON) tools/validate.py
	$(PYTHON) tools/validate_catalog.py
	$(PYTHON) tools/render_catalog.py --check
	$(PYTHON) -m unittest discover -s tests -v
