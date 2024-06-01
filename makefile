all: units type test analyse build

PYTHON := python3.12

.PHONY: units type test analyse build upload-test upload-pypi clean

units:
	$(PYTHON) -m make_catalogue --python noether/catalogue.py

analysis/output/:
	@mkdir analysis/output/

type: analysis/output/
	$(PYTHON) -m pyright --outputjson 2>/dev/null | jq '.generalDiagnostics[].file' -r | uniq | sed -e 's_.*Noether/__'| tee analysis/output/mistyped_files.txt

test: units
	$(PYTHON) -m unittest tests/*.py

analyse:
	$(PYTHON) -m unittest analysis/*.py

build: units analyse
	cd analysis/output && tar -c catalogue.* > catalogue.tar && mv catalogue.tar ..
	$(PYTHON) -m build

upload-test: test
	twine upload -u __token__ -p $$(cat token-test.txt) -r testpypi dist/*

upload-pypi: test
	twine upload -u __token__ -p $$(cat token-pypi.txt) dist/*

clean:
	$(PYTHON) make_units.py --remove
	rmdir analysis/output
	rmdir dist/
	rmdir noether.egg-info
