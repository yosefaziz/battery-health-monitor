#!/bin/bash

# stop on error
set -e

cd "$(dirname "$0")/.."

# avoid unsafe git error when running inside devcontainer
if [ -n "$DEVCONTAINER" ];then
  git config --global --add safe.directory "$PWD"
fi

# install/upgrade pre-commit
make pre-commit-install-all
