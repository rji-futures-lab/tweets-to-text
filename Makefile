init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	flake8 tweets2text/
	pipenv run py.test -v --cov=tweets2text/ tests/
