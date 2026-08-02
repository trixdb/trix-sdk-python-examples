#!/usr/bin/env bash
#
# Type-check the examples, use cases, and recipes.
#
# The numeric example directories (00_getting_started, 11_pipeline_presets, ...)
# are not valid Python package names, so mypy cannot analyse them as a single
# import tree — passing them together fails with either "not a valid Python
# package name" or "Duplicate module named 'main'". We therefore run mypy once
# per directory. Config (relaxed strictness) lives in pyproject.toml.
#
# Usage: scripts/typecheck.sh
set -u

status=0
for dir in examples/*/ use_cases/*/ recipes; do
    [ -d "$dir" ] || continue
    case "$dir" in
        *__pycache__*) continue ;;
    esac
    if ! mypy "$dir"; then
        status=1
    fi
done

if [ "$status" -eq 0 ]; then
    echo "typecheck: all directories passed"
fi
exit "$status"
