#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
PYTHONPATH=api python3 api/app/data/test.py
