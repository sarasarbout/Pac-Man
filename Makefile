
.PHONY: re fclean

fclean:
	rm -rf src/model/__pycache__
	rm -rf src/game/__pycache__
	rm -rf src/mazegenerator/__pycache__
	rm -rf src/mazegenerator/mazegenerator/__pycache__
	rm -rf src/parser/__pycache__
	rm -rf src/ui/__pycache__
	rm -rf src/draw/__pycache__
	rm -rf src/__pycache__

re: fclean
	PYTHONPATH=. .venv/bin/python -m src.main

run:
	.venv/bin/python -m src.main