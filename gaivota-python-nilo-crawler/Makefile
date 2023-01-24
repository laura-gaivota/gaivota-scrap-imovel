.DEFAULT_GOAL := install-all

help:
	@echo "check-dependencies       Check if all dependencies were satisfied."
	@echo "install                  Initialize the environment locally."
	@echo "install-all              Install everything locally, including poetry."
	@echo "install-dependencies     Install SO dependencies."
	@echo "install-precommit        Install pre-commit hooks."
	@echo "install-lint-tools       Install linters"
	@echo "lint                     Run project linters (falke8, isort and black)."
	@echo "test                     Run tests inside docker-compose dev container"
	@echo "docker-build             Build docker image gaivota_python_nilo_crawler:latest."
	@echo "docker-run               Run crawler on docker-compose dev container"
	@echo "docker-bash              Open a terminal in docker-compose dev container"

check-dependencies:
	@echo "###########################################################################"
	@echo "Checking dependencies."
	@echo "###########################################################################"
	@if ! command -v git ; then echo "Requirements: git is not installed"; exit 1; fi
	@if ! command -v pre-commit ; then echo "Requirements: pre-commit is not installed"; exit 1; fi
	@if ! command -v pip3 ; then echo "Requirements: pip3 is not installed"; exit 1; fi

install: check-dependencies
	@echo "###########################################################################"
	@echo "Installing git hooks and project dependencies."
	@echo "###########################################################################"
	@git init
	@pre-commit install -t pre-commit
	@pre-commit install -t pre-push

install-precommit:
	@echo "###########################################################################"
	@echo "Installing pre-commit hooks."
	@echo "###########################################################################"
	@curl https://pre-commit.com/install-local.py | python3 -
	@. ~/.profile

install-lint-tools:
	@echo "###########################################################################"
	@echo "Installing lint tools."
	@echo "###########################################################################"
	@pip3 install --user flake8
	@pip3 install --user isort
	@pip3 install --user black


install-dependencies: install-precommit
	@echo "###########################################################################"
	@echo "Installing dependencies."
	@echo "###########################################################################"
	# Add here any SO dependency needed by the project.

install-all: install-dependencies install-lint-tools install
	@echo "###########################################################################"
	@echo "Installing ALL environment."
	@echo "###########################################################################"

lint:
	@echo "###########################################################################"
	@echo "Verifying files with linter."
	@echo "###########################################################################"
	@python3 -m isort .
	@python3 -m black .
	@python3 -m flake8 .

test: lint
	@echo "###########################################################################"
	@echo "Starting tests."
	@echo "###########################################################################"
	@docker-compose run dev /root/.local/bin/pytest --disable-warnings --color=yes

coverage: lint
	@echo "###########################################################################"
	@echo "Starting coverage checking."
	@echo "###########################################################################"
	@docker-compose run dev /root/.local/bin/pytest --cov=python --disable-warnings --color=yes

profile:
	@echo "###########################################################################"
	@echo "Running profiling checks."
	@echo "###########################################################################"
	@echo "Profiling not implemented yet."

docker-build:
	@echo "###########################################################################"
	@echo "Building Docker image."
	@echo "###########################################################################"
	@docker build -t gaivota_python_nilo_crawler}:latest .
	@echo "Done."

docker-run: configure-database
	@echo "###########################################################################"
	@echo "Starting server on Docker container."
	@echo "###########################################################################"
	@docker-compose run dev /root/.local/bin/scrapy crawl nilo

docker-bash: configure-database
	@docker-compose run dev bash

configure-database:
	@docker-compose up -d database
	@git clone git@github.com:gaivota-ai/gaivota-postgres-db-layers.git -b $(git branch --show-current) || git clone git@github.com:gaivota-ai/gaivota-postgres-db-layers.git -b develop || true
	@docker run --network=host -v "$(pwd)/gaivota-postgres-db-layers/db:/db" -e DATABASE_URL=postgres://postgres:pass@127.0.0.1:2345/postgres?sslmode=disable amacneil/dbmate up || true
	@rm -rf gaivota-postgres-db-layers || true