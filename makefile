all: catalogue type test analyse build

catalogue:
	python3 noe_transformer.py

analysis/output/:
	@mkdir analysis/output/

type: analysis/output/
	python3 -m pyright --outputjson | jq '.generalDiagnostics[].file' -r | uniq | tee analysis/output/mistyped_files.txt

test:
	python3 -m unittest tests/*.py

analyse:
	python3 -m unittest analysis/*.py

build:
	tar -c analysis/output/catalogue.* > analysis/catalogue.tar
	# TODO #40

upload-test:
	# TODO #40

upload:
	# TODO #40

reset:
	bash -c "rm -r **/__pycache__"
	rm -r analysis/output
	python3 noe_transformer.py --remove
