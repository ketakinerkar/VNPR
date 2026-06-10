import tkinter as tk
from tkinter import messagebox as ms
from app.db.connection import get_connection
import re
import random


def open_user_register_window(parent):

    root = tk.Toplevel(parent)
    root.configure(background="black")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.title("User Registration")

    # -------- VARIABLES -------- #
    Fullname = tk.StringVar()
    address = tk.StringVar()
    username = tk.StringVar()
    Email = tk.StringVar()
    Phoneno = tk.StringVar()
    var = tk.IntVar()
    age = tk.IntVar()
    password = tk.StringVar()
    password1 = tk.StringVar()

    # -------- DB INIT -------- #
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            Fullname TEXT,
            address TEXT,
            username TEXT UNIQUE,
            Email TEXT,
            Phoneno TEXT,
            Gender INTEGER,
            age INTEGER,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

    # -------- VALIDATION -------- #
    def password_check(passwd):
        if len(passwd) < 6:
            return False
        if not any(c.isdigit() for c in passwd):
            return False
        if not any(c.isupper() for c in passwd):
            return False
        if not any(c.islower() for c in passwd):
            return False
        if not any(c in "$@#%" for c in passwd):
            return False
        return True

    # -------- MAIN FUNCTION -------- #
    def register_user():

        fname = Fullname.get()
        addr = address.get()
        uname = username.get()
        email = Email.get()
        mobile = Phoneno.get()
        gender = var.get()
        user_age = age.get()
        pwd = password.get()
        cpwd = password1.get()

        # validation
        if not fname or fname.isdigit():
            ms.showerror("Error", "Enter valid name")
            return

        if not addr:
            ms.showerror("Error", "Enter address")
            return

        if not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
            ms.showerror("Error", "Invalid email")
            return

        if not mobile.isdigit() or len(mobile) != 10:
            ms.showerror("Error", "Invalid phone")
            return

        if user_age <= 0 or user_age > 100:
            ms.showerror("Error", "Invalid age")
            return

        if not password_check(pwd):
            ms.showerror("Error", "Weak password")
            return

        if pwd != cpwd:
            ms.showerror("Error", "Passwords do not match")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (uname,))
            if cursor.fetchone():
                ms.showerror("Error", "Username already exists")
                return

            cursor.execute("""
                INSERT INTO users
                (Fullname, address, username, Email, Phoneno, Gender, age, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (fname, addr, uname, email, mobile, gender, user_age, pwd))

            conn.commit()
            conn.close()

            ms.showinfo("Success", "Account created successfully")

            # go back to login
            root.destroy()
            from app.ui.login import open_login_window
            open_login_window(parent)

        except Exception as e:
            ms.showerror("Error", str(e))

    # -------- UI -------- #

    tk.Label(root, text="USER REGISTRATION",
             font=("Times new roman", 25, "bold"),
             bg="black", fg="white").place(x=650, y=50)

    def label_entry(text, var, y):
        tk.Label(root, text=text, width=15,
                 font=("Times new roman", 15, "bold"),
                 bg="white").place(x=600, y=y)
        tk.Entry(root, textvariable=var,
                 width=20, font=('', 15)).place(x=830, y=y)

    label_entry("Full Name", Fullname, 150)
    label_entry("Address", address, 200)
    label_entry("Email", Email, 250)
    label_entry("Phone", Phoneno, 300)

    tk.Label(root, text="Gender", bg="white").place(x=600, y=350)
    tk.Radiobutton(root, text="Male", variable=var, value=1).place(x=830, y=350)
    tk.Radiobutton(root, text="Female", variable=var, value=2).place(x=950, y=350)

    label_entry("Age", age, 400)
    label_entry("Username", username, 450)

    tk.Label(root, text="Password", bg="white").place(x=600, y=500)
    tk.Entry(root, textvariable=password, show="*").place(x=830, y=500)

    tk.Label(root, text="Confirm Password", bg="white").place(x=600, y=550)
    tk.Entry(root, textvariable=password1, show="*").place(x=830, y=550)

    tk.Button(root, text="Register",
              bg="red", fg="white",
              font=("", 20),
              command=register_user).place(x=750, y=620)