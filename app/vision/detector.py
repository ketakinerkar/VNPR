import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import cv2
import os
from app.db.connection import get_connection
import smtplib
from email.mime.text import MIMEText
from google.cloud import vision
from ultralytics import YOLO
from fuzzywuzzy import process
from datetime import datetime
import requests


def start_detection(parent):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/vision.json"
    vision_client = vision.ImageAnnotatorClient()
    model = YOLO("models/license_plate_detector.pt")

    root = tk.Toplevel(parent)
    root.title("Number Plate Recognition System")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        ms.showerror("Error", "Camera not detected")
        return

    plate_data = {"img": None, "busy": False}

    def get_db():
        return get_connection()

    # ---------------- EMAIL ---------------- #
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

    # ---------------- CAMERA ---------------- #
    def update_frame():
        ret, frame = cap.read()

        if ret:
            results = model(frame)

            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                if conf > 0.5:
                    plate_crop = frame[y1:y2, x1:x2]
                    plate_data["img"] = plate_crop

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            canvas.create_image(0, 0, image=img, anchor=tk.NW)
            canvas.image = img

        canvas.after(10, update_frame)

    # ---------------- OCR ---------------- #
    def recognize_plate(img):
        _, enc = cv2.imencode('.jpg', img)
        response = vision_client.text_detection(
            image=vision.Image(content=enc.tobytes())
        )
        texts = response.text_annotations
        return texts[0].description.strip() if texts else None

    def format_plate(text):
        if text and text.startswith("IND"):
            text = text[3:]
        return ''.join(c for c in text if c.isalnum()).upper()

    def correct_plate(text):
        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT car_no FROM number_plates")
        stored = [r[0] for r in c.fetchall()]

        conn.close()

        print("STORED PLATES:", stored)

        if not stored:
            return text, 0

        match, score = process.extractOne(text, stored)
        print("MATCH:", match, "SCORE:", score)

        return match, score

    # ---------------- PROFILE ---------------- #
    def show_profile(data):
        Fullname, address, Email, Phoneno, Gender, age, photo, car_no, chassis = data[:9]

        print("PHOTO PATH:", photo)
        print("EXISTS:", os.path.exists(photo))

        frame = tk.LabelFrame(root, text="Profile", bg="skyblue")
        frame.place(x=600, y=150, width=650, height=400)

        details = [
            f"Name: {Fullname}",
            f"Email: {Email}",
            f"Phone: {Phoneno}",
            f"Car: {car_no}"
        ]

        y = 200
        for d in details:
            tk.Label(root, text=d, bg="white").place(x=650, y=y)
            y += 40

        try:
            if os.path.exists(photo):
                img = Image.open(photo)
                img = img.resize((150, 150))
                img = ImageTk.PhotoImage(img)

                lbl = tk.Label(root, image=img)
                lbl.image = img
                lbl.place(x=950, y=250)
            else:
                print("Image NOT found")

        except Exception as e:
            print("Image error:", e)

    # ---------------- LOG ---------------- #
    def log_entry_exit(car, email):

        print("\n--- LOG FUNCTION ---")
        print("CAR:", car)

        conn = get_db()
        c = conn.cursor()

        try:
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
            print("LAST ROW:", row)

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if row and row[1] is None:
                print("ACTION: EXIT")

                c.execute(
                    "UPDATE vehicle_logs SET exit_time=? WHERE id=?",
                    (now, row[0])
                )
                action = "Exit"

            else:
                print("ACTION: ENTRY")

                c.execute(
                    "INSERT INTO vehicle_logs (car_no, owner_email, entry_time) VALUES (?, ?, ?)",
                    (car, email, now)
                )
                action = "Entry"

            conn.commit()
            print("LOG SUCCESS")

        except Exception as e:
            print("DB ERROR:", e)

        finally:
            conn.close()

        send_email(email, action, f"{car} {action} at {now}")


    def call_api(image):
        _, img_encoded = cv2.imencode('.jpg', image)

        response = requests.post(
            "http://127.0.0.1:8000/detect",
            files={"file": img_encoded.tobytes()}
        )

        return response.json()

    # ---------------- MAIN ---------------- #
    def process_plate():

        if plate_data["busy"]:
            print("SKIPPED - BUSY")
            return

        plate_data["busy"] = True
        print("\n--- PROCESS START ---")

        img = plate_data["img"]

        if img is None:
            print("No plate detected")
            plate_data["busy"] = False
            return

        try:
            # 🔥 CALL BACKEND API
            result = call_api(img)

            print("API RESULT:", result)

            if result["status"] == "authorized":

                data = result["data"]

                show_profile(data)

            else:
                print("NOT AUTHORIZED:", result["status"])

        except Exception as e:
            print("API ERROR:", e)

        plate_data["busy"] = False
        print("--- PROCESS END ---\n")
    # ---------------- UI ---------------- #
    canvas = tk.Canvas(root, width=800, height=400)
    canvas.pack()

    tk.Button(root, text="Detect", command=process_plate).pack(pady=10)

    tk.Button(root, text="Exit",
              command=lambda: (cap.release(), root.destroy())).pack()

    update_frame()
    root.mainloop()