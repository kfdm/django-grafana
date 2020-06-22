PIP_BIN := .venv/bin/pip
APP_BIN := .venv/bin/django-admin

# Help 'function' taken from
# https://gist.github.com/prwhite/8168133#gistcomment-2278355

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20
.PHONY:	help
## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[\%a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

${PIP_BIN}:
	python3 -m venv .venv
	${PIP_BIN} install -U pip

${APP_BIN}: ${PIP_BIN}
	${PIP_BIN} install -e .

.PHONY: test
## Django: Run tests
test: ${APP_BIN}
	${APP_BIN} test -v 2

.PHONY: dist
dist:
	python3 setup.py sdist
