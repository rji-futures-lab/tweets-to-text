init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	pipenv run flake8 --extend-ignore W606 tweets2text/
	pipenv run py.test -v --cov=tweets2text/ tests/