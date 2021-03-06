.DEFAULT_GOAL := help

.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# Development

POETRY_INSTALL_EXTRAS = --extras "lint" --extras "test"
PYTEST_WATCH_ARGS = -vv
PYTEST_TEST_ARGS = $(PYTEST_WATCH_ARGS) --maxfail=2 -rf -vv --strict --cov src --cov-branch
PYTEST_ADDITIONAL_ARGS :=

.PHONY: install
install: install-clean  ## install the app

.PHONY: install-clean
install-clean:
	[ -f "poetry.lock" ] && rm "poetry.lock"
	poetry install --no-dev

.PHONY: install-ci
install-ci: ## install base and ci dependencies
	poetry install $(POETRY_INSTALL_EXTRAS) --no-dev

.PHONY: install-dev
install-dev: ## install base and dev dependencies
	poetry install $(POETRY_INSTALL_EXTRAS)

.PHONY: lint
lint: ## lint code
	poetry run flake8 src tests

.PHONY: tdd
tdd: ## start a TDD session (re-run test on saves)
	poetry run ptw -- $(PYTEST_WATCH_ARGS) $(PYTEST_ADDITIONAL_ARGS)

.PHONY: test
test: test-unit test-e2e  ## run all tests

.PHONY: test-e2e
test-e2e:  ## run end-to-end tests
	poetry run pytest test/e2e $(PYTEST_WATCH_ARGS) $(PYTEST_ADDITIONAL_ARGS)

.PHONY: test-unit
test-unit: ## run unit tests
	poetry run pytest test/unit $(PYTEST_TEST_ARGS) $(PYTEST_ADDITIONAL_ARGS)


# Release

CHANGELOG := CHANGELOG
VERSION = `cat pyproject.toml | grep "^version =" | cut -f 3 -d ' ' | cut -d '"' -f 2`

.PHONY: bump
bump:
	poetry version $(INCREMENT)

.PHONY: changelog
changelog:
	git-chglog -o $(CHANGELOG) -next-tag $(VERSION)

.PHONY: release
release: test
	$(MAKE) bump INCREMENT=$(INCREMENT)
	$(MAKE) changelog
	git add . && git commit -m "release: $(VERSION)" && git tag -a "$(VERSION)" -m $(VERSION)

.PHONY: major
major: ## release a new major
	$(MAKE) release INCREMENT='major'

.PHONY: minor
minor: ## release a new minor
	$(MAKE) release INCREMENT='minor'

.PHONY: patch
patch: ## release a new patch
	$(MAKE) release INCREMENT='patch'
