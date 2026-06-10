import tkinter as tk
from PIL import Image, ImageTk


def open_dashboard_window(parent):

    root = tk.Toplevel(parent)   # IMPORTANT
    root.title("Number Plate Recognition")

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    # Background
    background = Image.open('images/bg.jpg')
    background = background.resize((w, h), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(background)

    bg_label = tk.Label(root, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Title
    lbl = tk.Label(root,
                   text="Number Plate Recognition",
                   font=('Broadway', 30, 'bold'),
                   bg="Black", fg="white")
    lbl.place(x=0, y=0, width=1500)

    # -------- FUNCTIONS -------- #

    def open_register():
        from app.ui.vehicle_register import open_register_window
        open_register_window(root)

    def open_detection():
        from app.vision.detector import start_detection
        start_detection(root)

    def exit_app():
        root.destroy()

    # -------- BUTTONS -------- #

    button1 = tk.Button(root,
                        text='Number Plate Registration',
                        command=open_register,
                        font=('Times New Roman', 15, 'bold'),
                        width=25,
                        bg='purple', fg='white')
    button1.place(x=50, y=100)

    button2 = tk.Button(root,
                        text='Number Plate Recognition',
                        command=open_detection,
                        font=('Times New Roman', 15, 'bold'),
                        width=25,
                        bg='darkblue', fg='white')
    button2.place(x=50, y=160)

    exit_button = tk.Button(root,
                            text="Exit",
                            command=exit_app,
                            font=('Times New Roman', 15, 'bold'),
                            width=25,
                            bg='green', fg='linen')
    exit_button.place(x=50, y=220)