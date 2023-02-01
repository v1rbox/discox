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
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ifeq (remove,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

init:
	poetry install

run:
	$(PYTHON) -m bot

install-beautifier:
	@pip install black isort
	@echo "Successfully installed beautifier!"

beautify:
	@black .
	@echo "Successfully beautified code!"
	@isort .
	@echo "Successfully sorted imports!"

add:
	@echo "Adding new module..."
	@poetry add $(RUN_ARGS)
	@echo "Updating requirements.txt..."
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Successfully added new module!"

remove:
	@echo "Removing module..."
	@poetry remove $(RUN_ARGS)
	@echo "Updating requirements.txt..."
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Successfully removed module!"