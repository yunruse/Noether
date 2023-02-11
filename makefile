all: type analyse

type:
	python3 -m pyright --outputjson | jq '.generalDiagnostics[].file' -r | uniq | tee analysis/output/mistyped_files.txt

analyse:
	python3 -m unittest analysis/*.py
	tar -c analysis/output/catalogue.* > analysis/catalogue.tar

clean:
	rm -r analysis/output