import os
import subprocess
from pathlib import Path

import pytesseract
from PIL import Image
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def show_popup(title: str, text: str) -> None:
    subprocess.run(["kdialog", "--title", title, "--msgbox", text], check=False)

def translate_en_to_th(text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict formatter.\n"
                    "Your job is to ALWAYS output EXACTLY 3 lines, no more, no less.\n"
                    "You MUST include the labels exactly as written.\n\n"
                    "OUTPUT FORMAT (MUST FOLLOW EXACTLY):\n"
                    "English: <original input>\n"
                    "ภาษาไทย: <thai translation>\n"
                    "ความหมาย: <short Thai meaning explanation>\n\n"
                    "RULES:\n"
                    "- NEVER omit 'ภาษาไทย:'\n"
                    "- NEVER rename labels\n"
                    "- NEVER add extra text before or after\n"
                    "- Meaning must be in Thai, 1–2 short sentences\n"
                    "- If input is unclear or nonsense, still keep the format and use '(ไม่ชัดเจน)'\n"
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

def ocr_image(path: str | Path, lang: str = "eng") -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    img = Image.open(path)
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(img, lang=lang, config=config)
    return text.strip()

def capture_with_spectacle_region() -> Path:
    images_dir = Path(__file__).resolve().parent / "images_temp"
    images_dir.mkdir(parents=True, exist_ok=True)

    output_path = images_dir / "capture.png"

    subprocess.run(
        ["spectacle", "--background", "--nonotify", "--region", "--output", str(output_path)],
        check=True,
    )

    if not output_path.exists():
        raise RuntimeError("Spectacle capture failed (no output file created)")
    return output_path

def main():
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Missing GROQ_API_KEY environment variable")

    img_path = capture_with_spectacle_region()
    print(f"Saved screenshot: {img_path}")

    extracted = ocr_image(img_path, lang="eng")
    if not extracted:
        print("OCR returned empty text.")
        return
    
    thai = translate_en_to_th(extracted)
    show_popup("Thai Translation", thai)

if __name__ == "__main__":
    main()