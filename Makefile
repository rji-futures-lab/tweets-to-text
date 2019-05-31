init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	pipenv run flake8 --extend-ignore W606 tweets2text/
	pipenv run py.test -v --cov=tweets2text/ tests/

localdynamodb:
	wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz -O /tmp/dynamodb_local_latest.tar.gz
	mkdir /tmp/dynamodb/
	tar -xzf /tmp/dynamodb_local_latest.tar.gz -C /tmp/dynamodb/
