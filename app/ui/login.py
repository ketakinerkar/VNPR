import tkinter as tk
from tkinter import messagebox as ms
from app.db.connection import get_connection
from PIL import Image, ImageTk


def open_login_window(parent):

    root = tk.Toplevel(parent)
    root.configure(background="pink")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    username = tk.StringVar()
    password = tk.StringVar()

    # Background
    image2 = Image.open('images/bg.jpg')
    image2 = image2.resize((w, h), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)

    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)

    # -------- FUNCTIONS -------- #

    def open_user_register():
        from app.ui.user_register import open_user_register_window
        open_user_register_window(root)

    def open_dashboard(parent_window):
        from app.ui.dashboard import open_dashboard_window
        open_dashboard_window(parent_window)

    def login():

        uname = username.get()
        pwd = password.get()

        if not uname or not pwd:
            ms.showerror("Error", "Enter username and password")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # ✅ USE USERS TABLE (FIXED)
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

            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (uname, pwd)
            )

            result = cursor.fetchone()

            conn.close()

            if result:
                ms.showinfo("Success", "Login successful")
                parent_window = parent
                root.destroy()
                open_dashboard(parent_window)
            else:
                ms.showerror("Error", "Invalid username or password")

        except Exception as e:
            ms.showerror("Error", str(e))

    # -------- UI -------- #

    login_frame = tk.Frame(root, bg="grey")
    login_frame.place(x=500, y=220)

    tk.Label(login_frame, text="Login Here",
             font=("Times new roman", 20, "bold"),
             bg="grey").grid(row=0, columnspan=2, pady=10)

    tk.Label(login_frame, text="Username",
             font=("Times new roman", 20, "bold"),
             bg="grey").grid(row=1, column=0, padx=20, pady=10)

    tk.Entry(login_frame, textvariable=username,
             font=("", 15)).grid(row=1, column=1, padx=20)

    tk.Label(login_frame, text="Password",
             font=("Times new roman", 20, "bold"),
             bg="grey").grid(row=2, column=0, padx=20, pady=10)

    tk.Entry(login_frame, textvariable=password,
             show="*", font=("", 15)).grid(row=2, column=1, padx=20)

    tk.Button(login_frame, text="Login",
              command=login,
              width=15,
              font=("Times new roman", 14, "bold"),
              bg="blue", fg="white").grid(row=3, column=1, pady=10)

    tk.Button(login_frame, text="Create Account",
              command=open_user_register,   # ✅ FIXED
              width=15,
              font=("Times new roman", 14, "bold"),
              bg="red").grid(row=3, column=0, pady=10)