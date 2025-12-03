# Ollama Typhoon OCR

A Python-based OCR API using **FastAPI** and **scb10x/typhoon-ocr-3b** for extracting text from images

---

## Installation

1) Clone Repository
```bash
git clone https://github.com/devph4t/python-ollama-typhoon-ocr.git
cd python-ollama-typhoon-ocr
```

2) Pull & Run Typhoon OCR Model
```bash
ollama run scb10x/typhoon-ocr-3b:latest
```

3) Install Dependencies
```bash
uv add -r requirements.txt
```

4) Start FastAPI Server
```bash
make run
```
Server is running on:
👉 http://localhost:3000/
