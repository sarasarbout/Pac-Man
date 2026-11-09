
.PHONY: install run debug clean re lint uninstall

install:
	@if [ ! -f mazegenerator-00001.zip ]; then \
		echo "Error: mazegenerator-00001.zip not found!"; \
		exit 1; \
	fi
	python3 -m venv .venv
	unzip -o mazegenerator-00001.zip
	.venv/bin/python -m pip install -r requirements.txt

clean:
	rm -rf src/model/__pycache__
	rm -rf src/game/__pycache__
	rm -rf src/mazegenerator/__pycache__
	rm -rf src/mazegenerator/mazegenerator/__pycache__
	rm -rf src/parser/__pycache__
	rm -rf src/ui/__pycache__
	rm -rf src/draw/__pycache__
	rm -rf src/__pycache__
	rm -rf .mypy_cache
	rm -rf src/.mypy_cache

run:
	.venv/bin/python pac-man.py src/config.json

debug:
	.venv/bin/python -m pdb pac-man.py src/config.json

re: clean run

lint:
	flake8 . --exclude=.git,__pycache__,.venv,build,dist,.tox,.eggs,*.egg \
		&& mypy . --explicit-package-bases --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
uninstall:
	rm -rf .venv
	rm -rf mazegenerator-2.1.0-py3-none-any.whl
