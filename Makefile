.PHONY: install run test

PYTHON ?= python
HOST ?= 127.0.0.1
PORT ?= 8000

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn app.main:app --host $(HOST) --port $(PORT) --reload

test:
	$(PYTHON) -m pytest tests/test_task_service.py tests/test_priority_advisor.py tests/test_task_routes.py
