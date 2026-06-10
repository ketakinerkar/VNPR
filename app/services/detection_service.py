import cv2
import os
from ultralytics import YOLO
from google.cloud import vision
from fuzzywuzzy import process
from app.db.connection import get_connection
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/vision.json"

model = YOLO("models/license_plate_detector.pt")
vision_client = vision.ImageAnnotatorClient()


def detect_plate(frame):

    results = model(frame)

    plate_crop = None

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_crop = frame[y1:y2, x1:x2]
        break   # take first detected plate

    if plate_crop is None:
        return {"status": "no_plate"}

    # OCR
    _, enc = cv2.imencode('.jpg', plate_crop)
    texts = vision_client.text_detection(
        image=vision.Image(content=enc.tobytes())
    ).text_annotations

    if not texts:
        return {"status": "ocr_failed"}

    raw_text = texts[0].description.strip()
    formatted = ''.join(c for c in raw_text if c.isalnum()).upper()

    # DB match
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT car_no FROM number_plates")
    stored = [r[0] for r in c.fetchall()]

    if not stored:
        conn.close()
        return {"status": "no_registered"}

    result_match = process.extractOne(formatted, stored)

    if not result_match:
        return {"status": "no_match"}

    match, score = result_match

    c.execute("SELECT * FROM number_plates WHERE car_no=?", (match,))
    result = c.fetchone()

    conn.close()

    if not result:
        return {"status": "unauthorized"}

    log_entry_exit(match, result[2])

    return {
        "status": "authorized",
        "detected": formatted,
        "corrected": match,
        "confidence": score,
        "data": result
    }


def send_email(recipient, subject, body):
    sender_email = "vehicle452@gmail.com"
    sender_password = "xffm ygbq qaqx gicn"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
    except Exception as e:
        print("Email error:", e)


def log_entry_exit(car, email):


    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_no TEXT,
        owner_email TEXT,
        entry_time TEXT,
        exit_time TEXT
    )
    """)

    c.execute(
        "SELECT id, exit_time FROM vehicle_logs WHERE car_no=? ORDER BY id DESC LIMIT 1",
        (car,)
    )

    row = c.fetchone()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if row and row[1] is None:
        c.execute(
            "UPDATE vehicle_logs SET exit_time=? WHERE id=?",
            (now, row[0])
        )
        action = "Exit"
    else:
        c.execute(
            "INSERT INTO vehicle_logs (car_no, owner_email, entry_time) VALUES (?, ?, ?)",
            (car, email, now)
        )
        action = "Entry"

    conn.commit()
    conn.close()

    send_email(email, action, f"{car} {action} at {now}")