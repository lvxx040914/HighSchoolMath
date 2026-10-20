PYTHON ?= python3
.PHONY: validate test generate student teacher build clean

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
