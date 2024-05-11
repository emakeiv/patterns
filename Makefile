install:
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	# format code
	black tests/*.py src/*/*.py
lint:
	# code linting 
	pylint --disable=R,C src/*.py test/*.py
test:
	python -m pytest -vv --cov=src tests/*.py
build:
	# build container
deploy:
	#deploy onto cloud
all: install lint test build deploy