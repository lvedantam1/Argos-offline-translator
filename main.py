from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from translator import translate_text, extract_text_from_pdf, extract_text_from_txt

app = FastAPI(title="Offline Translator (Datacap PDFs Supported)")

# -------------------------------
# Pydantic Models
# -------------------------------
class TranslateRequest(BaseModel):
    text: str
    from_lang: str = None  # Optional — auto-detect if missing


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str


# -------------------------------
# API Endpoints
# -------------------------------
@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    """Translate plain text provided in the request body."""
    try:
        translated = translate_text(req.text, req.from_lang)
        return TranslateResponse(original_text=req.text, translated_text=translated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate-file", response_model=TranslateResponse)
async def translate_file(file: UploadFile = File(...)):
    """
    Upload a .txt or Datacap PDF file, automatically extract text,
    detect the source language, and translate it to English.
    """
    try:
        filename = file.filename.lower()

        if filename.endswith(".txt"):
            text_content = extract_text_from_txt(file.file)

        elif filename.endswith(".pdf"):
            text_content = extract_text_from_pdf(file.file)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload .txt or .pdf only.")

        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in the file.")

        # Auto-detect language and translate
        translated = translate_text(text_content)
        return TranslateResponse(original_text=text_content, translated_text=translated)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
