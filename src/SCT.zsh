#!/usr/bin/env zsh
set -e

# Folder where this .zsh file lives (src/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Project root (one level up from src/)
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Use venv python from project root
PYTHON="$PROJECT_DIR/venv/bin/python"
MAIN="$SCRIPT_DIR/main.py"

# Optional: keep temp images inside src/images_temp
mkdir -p "$SCRIPT_DIR/images_temp"

exec "$PYTHON" "$MAIN"