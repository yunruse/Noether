all: units type test analyse build

units:
	python3 make_units.py

analysis/output/:
	@mkdir analysis/output/

type: analysis/output/
	python3 -m pyright --outputjson 2>/dev/null | jq '.generalDiagnostics[].file' -r | uniq | sed -e 's_.*Noether/__'| tee analysis/output/mistyped_files.txt

test:
	python3 -m unittest tests/*.py

analyse:
	python3 -m unittest analysis/*.py

build:
	cd analysis/output && tar -c catalogue.* > catalogue.tar && mv catalogue.tar ..

upload-test:
	# TODO #40

upload:
	# TODO #40

reset:
	bash -c "rm -r **/__pycache__"
	rm -r analysis/output
	python3 noe_transformer.py --remove
