PYTHON = .\.venv\Scripts\python.exe

run:
	$(PYTHON) -m uvicorn main:app --reload --port 3000