import os
import sqlite3
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import easyocr
import io
import asyncio

print("Loading environment variables...")
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MONITOR_GROUP_ID = int(os.getenv("MONITOR_GROUP_ID"))

keywords_string = os.getenv("FRAUD_KEYWORDS", "")
FRAUD_KEYWORDS_LIST = [keyword.strip().lower() for keyword in keywords_string.split(',')]

print(f"Monitoring {len(FRAUD_KEYWORDS_LIST)} keywords: {FRAUD_KEYWORDS_LIST}")

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
reader = None

def init_db():
    conn = sqlite3.connect('fraud_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message_text TEXT,
            ocr_result TEXT,
            is_alert BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(text, ocr, alert):
    conn = sqlite3.connect('fraud_database.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (message_text, ocr_result, is_alert) VALUES (?, ?, ?)",
        (text, ocr, alert)
    )
    conn.commit()
    conn.close()

def check_text_for_fraud(text_to_check):
    if not text_to_check:
        return False
    text_lower = text_to_check.lower()
    for keyword in FRAUD_KEYWORDS_LIST:
        if keyword in text_lower:
            return True
    return False

def process_image_from_bytes(image_bytes):
    try:
        results = reader.readtext(image_bytes)
        extracted_text = " ".join([text for (bbox, text, prob) in results])
        is_alert = check_text_for_fraud(extracted_text)
        return extracted_text, is_alert
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return "", False

@app.on_message(filters.chat(MONITOR_GROUP_ID) & (filters.text | filters.photo))
async def handle_message(client: Client, message: Message):
    while reader is None:
        print("Handler waiting for the OCR reader to initialize...")
        await asyncio.sleep(1)

    print(f"New message received: ID {message.id}")

    original_text = message.text or (message.caption if message.caption else "")
    ocr_result = ""
    is_alert = check_text_for_fraud(original_text)

    if message.photo:
        print(f"Processing image in memory using OCR...")
        image_bytes_io = await message.download(in_memory=True)
        ocr_result, ocr_alert = process_image_from_bytes(image_bytes_io.getvalue())
        if ocr_alert:
            is_alert = True

    if is_alert:
        print("="*40)
        print(f"🚨 FRAUD ALERT DETECTED! (Message ID: {message.id}) 🚨")
        if original_text:
            print(f"Text: {original_text[:200]}...")
        if ocr_result:
            print(f"OCR: {ocr_result[:200]}...")
        print("="*40)

    if message.text or message.photo:
        save_to_db(original_text, ocr_result, is_alert)

async def main():
    global reader
    print("Initializing monitor...")
    init_db()
    await app.start()
    print("Loading OCR model (EasyOCR)...")
    reader = easyocr.Reader(['en', 'pt'], gpu=False)
    print("EasyOCR reader initialized successfully.")
    print("Monitor online. Listening for new messages...")
    await idle()

if __name__ == "__main__":
    app.run(main())
