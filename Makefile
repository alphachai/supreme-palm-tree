export COMPOSE_SERVICE_NAME=supreme-palm-tree

-include $(shell [ -e .build-harness ] || curl -sSL -o .build-harness "https://git.io/mintel-build-harness"; echo .build-harness)

init: bh/init
	@$(MAKE) bh/venv pipenv
.PHONY: init

.env:
	@read -p "Enter a port for your dev site: " DEV_PORT; \
	echo "# Port for dev site. Must end in a colon (:)." >> .env; \
	echo "DEV_PORT=$$DEV_PORT:" >> .env; \
	echo "Wrote DEV_PORT=$$DEV_PORT: to .env" 1>&2;
	echo "DEBUG=true" >> .env

up: .env compose/up
.PHONY: up

down: .env compose/down
.PHONY: down

restart: compose/restart
.PHONY: restart

rebuild: compose/rebuild
.PHONY: rebuild

exec: docker/exec
.PHONY: exec

ps: compose/ps
.PHONY: ps

logs: compose/logs
.PHONY: logs

tail: logs
.PHONY: tail

lint: python/lint
.PHONY: lint

fmt: python/fmt
.PHONY: fmt

scan: python/scan
.PHONY: scan

test: pytest
.PHONY: test

clean: pipenv/clean python/clean
	@exit 0
.PHONY: clean
