install:
	rm -r dist
	poetry build
	pip install dist/*.whl
