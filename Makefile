# pre-commit tasks

pre-commit-all: ## execute all pre-commit hooks
	pre-commit run --all-files

pre-commit-install-all: pre-commit-install pre-commit-install-cmt-hook pre-commit-install-hooks

pre-commit-install-hooks:
	pre-commit install --install-hooks

pre-commit-install-cmt-hook:
	pre-commit install --hook-type commit-msg

pre-commit-install:
	pre-commit install

pre-commit-update:
	pre-commit autoupdate


# terraform deployment
terraform-check: terraform-fmt terraform-validate

terraform-run-dev: terraform-init-dev terraform-plan-dev terraform-apply-dev

terraform-init-dev:
	terraform -chdir=./deployments/environments/dev init

terraform-plan-dev:
	terraform -chdir=./deployments/environments/dev plan

terraform-apply-dev:
	terraform -chdir=./deployments/environments/dev apply

terraform-fmt:
	terraform fmt -recursive

terraform-validate:
	terraform validate
