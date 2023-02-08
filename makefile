all: analysis/output/catalogue.tar

analysis/output/catalogue.tar: analyse
analyse: analysis/output/catalogue.json
	python3 -m unittest analysis/*.py
	tar -c analysis/output/catalogue.* > analysis/catalogue.tar


clean:
	rm -r analysis/output