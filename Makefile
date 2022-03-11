types:
	mypy .

format:
	black .
	isort --atomic .

style:
	flake8 .

lint:
	make format style types

install:
	pip install -r requirements.txt
