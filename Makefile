TRASH_CMD_PATH = $(which trash)

ifdef TRASH_CMD_PATH
	RM = trash
endif

.PHONY: help
help:
	@echo "Usage: make [prettify|prune|test]"
	@echo ""
	@grep -E '^[/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | perl -pe 's%^([/a-zA-Z_-]+):.*?(##)%$$1 $$2%' | awk -F " *?## *?" '{printf "\033[36m%-30s\033[0m %-50s %s\n", $$1, $$2, $$3}'

.PHONY: prettify
prettify: ## Prettify the project files
	find . -name ".tox" -type d -o -name ".venv" -type d -prune -o -name "*.py" -print0 | xargs -0 -P 12 -L 1 black -q

.PHONY: prune
prune: ## Prune the project files
	find . -type d -name "*.egg"       -print0 | xargs -0 $(RM)
	find . -type d -name "*.egg-info"  -print0 | xargs -0 $(RM)
	find . -type d -name ".tox"        -print0 | xargs -0 $(RM)
	find . -type d -name "__pycache__" -print0 | xargs -0 $(RM)
	find . -type d -name "build"       -print0 | xargs -0 $(RM)
	find . -type f -name "*.pyc"       -print0 | xargs -0 $(RM)

.PHONY: test
test: ## Run the testing
	command -v tox || pip install tox==3.28.0
	find . -maxdepth 1 -name "lambda_*" -type d -print0 | xargs -0 -I % -P 6 sh -c "cd % && tox"
