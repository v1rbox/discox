POETRY_PYTHON_PATH = $(shell poetry env info --path)
POETRY_PYTHON_PATH := $(subst  ,,$(POETRY_PYTHON_PATH)) # remove spaces
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON = $(addsuffix \Scripts\python.exe,$(POETRY_PYTHON_PATH))
else
	# Linux
	PYTHON = $(addsuffix /bin/python,$(POETRY_PYTHON_PATH))
endif

ifeq (add,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

init:
	poetry install

run:
	$(PYTHON) -m bot

install-beautifier:
	pip install black isort

beautify:
	black .
	isort .

add:
	@echo "Adding new module..."
	poetry add $(RUN_ARGS)
	poetry export -f requirements.txt --output requirements.txt --without-hashes