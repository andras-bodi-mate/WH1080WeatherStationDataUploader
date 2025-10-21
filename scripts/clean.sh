#!/bin/bash
(cd ../
uv run python3 src/main.py clean || { \
    echo "Uv was not found. Installing..."; \
    curl -LsSf https://astral.sh/uv/install.sh | sh; \
    echo "Installation complete. Please restart this script to continue."; \
    exit 1; \
})