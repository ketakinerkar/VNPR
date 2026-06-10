import tkinter as tk
from PIL import Image, ImageTk


def start_app():
    root = tk.Tk()
    root.title("Number Plate System")
    root.geometry("1600x900")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()

    # Background
    bg = Image.open("images/bg.jpg")
    bg_img = ImageTk.PhotoImage(bg)
    bg_lbl = tk.Label(root, image=bg_img)
    bg_lbl.place(x=0, y=93, relwidth=1, relheight=1)

    # Logo animation
    img1 = ImageTk.PhotoImage(Image.open("images/1.jpg"))
    img2 = ImageTk.PhotoImage(Image.open("images/2.jpg"))
    img3 = ImageTk.PhotoImage(Image.open("images/3.jpg"))

    logo_label = tk.Label(root)
    logo_label.place(x=60, y=200)

    x = 1

    def move():
        nonlocal x
        if x == 4:
            x = 1
        if x == 1:
            logo_label.config(image=img1)
        elif x == 2:
            logo_label.config(image=img2)
        elif x == 3:
            logo_label.config(image=img3)
        x += 1
        root.after(1000, move)

    move()

    # Welcome text
    wlcm = tk.Label(root, text="Drive for safety..save life",
                    font=("Roboto", 22, "bold"), bg='white')
    wlcm.place(x=200, y=150)

    # Navigation functions (IMPORTANT CHANGE)

    def open_login():
        from app.ui.login import open_login_window
        open_login_window(root)

    def open_register():
        from app.ui.user_register import open_user_register_window
        open_user_register_window(root)

    # Buttons
    btn_login = tk.Button(root, text="Login",
                          command=open_login,
                          width=20, height=2,
                          bg="white", fg="#6e336b",
                          font=("times new roman", 14, "bold"))
    btn_login.place(x=1100, y=350)

    btn_register = tk.Button(root, text="Register",
                             command=open_register,
                             width=20, height=2,
                             bg="white", fg="#6e336b",
                             font=("times new roman", 14, "bold"))
    btn_register.place(x=1100, y=450)

    root.mainloop()