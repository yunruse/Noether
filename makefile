all: units type test analyse build

.PHONY: units type test analyse build upload-test upload-pypi clean

units:
	poetry run python make_units.py

analysis/output/:
	@mkdir analysis/output/

type: analysis/output/
	poetry run python -m pyright --outputjson 2>/dev/null | jq '.generalDiagnostics[].file' -r | uniq | sed -e 's_.*Noether/__'| tee analysis/output/mistyped_files.txt

test: units
	poetry run python -m unittest tests/*.py

analyse:
	poetry run python -m unittest analysis/*.py

build: units analyse
	cd analysis/output && tar -c catalogue.* > catalogue.tar && mv catalogue.tar ..
	poetry run python -m build

upload-test: test
	twine upload -u __token__ -p $$(cat token-test.txt) -r testpypi dist/*

upload-pypi: test
	twine upload -u __token__ -p $$(cat token-pypi.txt) dist/*

clean:
	python3 make_units.py --remove
	rmdir analysis/output
	rmdir dist/
	rmdir noether.egg-info
