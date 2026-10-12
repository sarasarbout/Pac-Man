fclean:
	rm -rf model/__pycache__
	rm -rf game/__pycache__
	rm -rf mazegenerator/__pycache__
	rm -rf mazegenerator/mazegenerator/__pycache__

re: fclean
	PYTHONPATH=.:mazegenerator python3 src/draw/generate.py