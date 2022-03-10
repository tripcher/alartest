types:
	mypy .

format:
	black .
	isort --atomic .

style:
	flake8 .

lint:
	make format style types


install-dev:
	pip install -r requirements.txt
	pip install -r requirements_dev.txt

install:
	pip install -r requirements.txt
