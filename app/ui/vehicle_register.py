import tkinter as tk
from tkinter import messagebox as ms
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import re
import os
import uuid
from app.db.connection import get_connection


def open_register_window(parent):

    window = tk.Toplevel(parent)
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.title("Number Plate Registration")
    window.configure(background="grey")

    # -------- VARIABLES -------- #
    Fullname = tk.StringVar()
    address = tk.StringVar()
    Email = tk.StringVar()
    Phoneno = tk.StringVar()
    var = tk.IntVar()
    age = tk.IntVar()
    carno = tk.StringVar()
    chassis = tk.StringVar()
    file_path = {"path": None}

    # -------- IMAGE SELECT -------- #
    def show():
        path = askopenfilename(
            title='Select Image',
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if path:
            file_path["path"] = path
            try:
                image = Image.open(path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(image)
                preview_label.config(image=img)
                preview_label.image = img
            except Exception as e:
                ms.showerror("Error", f"Cannot open image: {e}")

    # -------- MAIN FUNCTION -------- #
    def insert_data():

        fname = Fullname.get()
        addr = address.get()
        email = Email.get()
        mobile = Phoneno.get()
        gender = var.get()
        user_age = age.get()
        car_no = carno.get().upper()
        chassis_no = chassis.get()

        # -------- VALIDATION -------- #
        if not fname or not addr or not email or not mobile or not car_no or not chassis_no or not file_path["path"]:
            ms.showerror("Error", "All fields required")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            ms.showerror("Error", "Invalid email")
            return

        if not mobile.isdigit() or len(mobile) != 10:
            ms.showerror("Error", "Invalid phone")
            return

        try:
            # -------- SAVE IMAGE TO FOLDER -------- #
            os.makedirs("uploads", exist_ok=True)

            ext = os.path.splitext(file_path["path"])[1]

            # unique filename (prevents overwrite)
            filename = f"{car_no}_{uuid.uuid4().hex[:6]}{ext}"

            dest_path = os.path.abspath(os.path.join("uploads", filename))
            print(dest_path)

            with open(file_path["path"], "rb") as src:
                with open(dest_path, "wb") as dst:
                    dst.write(src.read())

            # -------- DB -------- #
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS number_plates(
                    Fullname TEXT,
                    address TEXT,
                    Email TEXT,
                    Phoneno TEXT,
                    Gender INTEGER,
                    age INTEGER,
                    photo TEXT,
                    car_no TEXT,
                    chassis_no TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicle_logs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_no TEXT,
                    owner_email TEXT,
                    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    exit_time TIMESTAMP
                )
            """)

            cursor.execute("""
                INSERT INTO number_plates
                (Fullname, address, Email, Phoneno, Gender, age, photo, car_no, chassis_no)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fname, addr, email, mobile, gender, user_age, dest_path, car_no, chassis_no))

            conn.commit()
            conn.close()

            ms.showinfo("Success", "Vehicle Registered Successfully")
            window.destroy()

        except Exception as e:
            ms.showerror("Error", str(e))

    # -------- UI -------- #

    # Background
    image2 = Image.open('images/r.webp')
    image2 = image2.resize((w, h), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(image2)

    bg_label = tk.Label(window, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0)

    tk.Label(window, text="Number Plate Registration Form",
             font=("Times new roman", 30, "bold"),
             bg="#192841", fg="white").place(x=480, y=50)

    def label_entry(text, var, y):
        tk.Label(window, text=text, bg="white",
                 font=("Times new roman", 12, "bold")).place(x=600, y=y)
        tk.Entry(window, textvariable=var,
                 font=("", 12)).place(x=830, y=y)

    label_entry("Full Name", Fullname, 150)
    label_entry("Address", address, 200)
    label_entry("Email", Email, 250)
    label_entry("Phone", Phoneno, 300)

    tk.Label(window, text="Gender", bg="white").place(x=600, y=350)
    tk.Radiobutton(window, text="Male", variable=var, value=1).place(x=830, y=350)
    tk.Radiobutton(window, text="Female", variable=var, value=2).place(x=950, y=350)

    label_entry("Age", age, 400)
    label_entry("Car Number", carno, 450)
    label_entry("Chassis Number", chassis, 500)

    tk.Button(window, text="Upload Photo",
              command=show, bg="blue", fg="white").place(x=600, y=550)

    preview_label = tk.Label(window)
    preview_label.place(x=850, y=520)

    tk.Button(window, text="Register",
              command=insert_data,
              bg="green", fg="white",
              font=("Times new roman", 14, "bold")).place(x=700, y=620)