import pdfplumber
from langdetect import detect
from argostranslate import translate, package

# -------------------------------
# Argos Translate Configuration
# -------------------------------
package.update_package_index()
SUPPORTED_LANGUAGES = ["en", "fr", "es", "ja"]


# -------------------------------
# Helper Functions
# -------------------------------
def get_installed_languages():
    """Return list of installed Argos Translate languages."""
    return translate.get_installed_languages()


def install_model_if_missing(from_lang: str, to_lang: str):
    """Install translation model if not already available."""
    installed_languages = get_installed_languages()
    src = next((l for l in installed_languages if l.code == from_lang), None)
    tgt = next((l for l in installed_languages if l.code == to_lang), None)

    if src and tgt:
        return

    available_packages = package.get_available_packages()
    pkg = next(
        (p for p in available_packages if p.from_code == from_lang and p.to_code == to_lang),
        None
    )
    if pkg:
        print(f"Installing model for {from_lang} → {to_lang} ...")
        pkg.install()
    else:
        raise Exception(f"No Argos Translate model found for {from_lang} → {to_lang}")


def extract_text_from_pdf(file) -> str:
    """Extract text content from a PDF file."""
    text_content = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() or ""
    return text_content.strip()


def extract_text_from_txt(file) -> str:
    """Extract text content from a plain text (.txt) file."""
    content = file.read().decode("utf-8", errors="ignore")
    return content.strip()


def translate_text(text: str, from_lang: str = None, to_lang: str = "en") -> str:
    """Translate text from one language to another using Argos Translate."""
    if not from_lang:
        from_lang = detect(text)
    from_lang = from_lang[:2]  # Normalize to 2-letter ISO code

    if from_lang not in SUPPORTED_LANGUAGES:
        raise Exception(f"Unsupported source language '{from_lang}'. Supported: {SUPPORTED_LANGUAGES}")

    if to_lang not in SUPPORTED_LANGUAGES:
        raise Exception(f"Unsupported target language '{to_lang}'. Supported: {SUPPORTED_LANGUAGES}")

    install_model_if_missing(from_lang, to_lang)

    installed_languages = get_installed_languages()
    src_lang = next((l for l in installed_languages if l.code == from_lang), None)
    tgt_lang = next((l for l in installed_languages if l.code == to_lang), None)

    if not src_lang or not tgt_lang:
        raise Exception(f"Language pair {from_lang} → {to_lang} not found after installation")

    translation = src_lang.get_translation(tgt_lang)
    return translation.translate(text)
