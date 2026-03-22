#!/bin/bash
# Automatically run MS SQL Alembic schema migrations exactly before booting
alembic upgrade head

# Boot the highly optimized ASGI server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
