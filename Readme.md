# Offline Translator

This project provides an **offline translation service** for Datacap-extracted text using **Argos Translate**.

## Features
- Translate text from French, Spanish, Japanese, and English to English.
- Supports `.txt` and PDF files.
- Uses Argos Translate offline models.
- Auto-detects source language.

## Requirements
- Python 3.11
- Argos Translate models for required languages

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
