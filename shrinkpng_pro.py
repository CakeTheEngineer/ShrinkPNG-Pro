import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pystray import Icon, MenuItem, Menu
from PIL import Image
import subprocess
import requests
import shutil
import tempfile

VERSION = "0.9.0"

def check_update():
    try:
        r = requests.get("https://raw.githubusercontent.com/CakeTheEngineer/ShrinkPNG-Pro/main/version.json")
        data = r.json()
        if data["version"] != VERSION:
            if messagebox.askyesno("Update Available", "New version available. Update now?"):
                update_url = data["url"]
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
                with requests.get(update_url, stream=True) as u:
                    with open(tmp.name, 'wb') as f:
                        shutil.copyfileobj(u.raw, f)
                os.startfile(tmp.name)
                sys.exit()
    except:
        pass

def compress_file(path):
    if os.path.getsize(path) > 10 * 1024 * 1024:
        out = path.replace(".png", "_compressed.png")
        subprocess.run(["oxipng", "-o", "4", "--strip", "safe", path, "-o", out], shell=True)
        print("Compressed:", path)

def on_folder_select():
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.endswith(".png"):
                compress_file(os.path.join(folder, file))
        messagebox.showinfo("Done", "Compression complete.")

def build_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.geometry("400x250")
    app.title("ShrinkPNG Pro BETA")

    def tray_exit():
        tray.stop()
        app.destroy()

    def minimize():
        app.withdraw()

    def restore():
        app.deiconify()

    image = Image.open("icon.png").resize((64, 64))
    menu = Menu(MenuItem("Open", lambda: restore()), MenuItem("Exit", lambda: tray_exit()))
    tray.icon = image
    tray.menu = menu
    threading.Thread(target=tray.run).start()

    ctk.CTkLabel(app, text="ShrinkPNG Pro BETA", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(app, text="Wybierz folder z PNG", command=on_folder_select).pack(pady=10)
    ctk.CTkButton(app, text="Minimalizuj do tray", command=minimize).pack(pady=5)

    check_update()
    app.mainloop()

tray = Icon("ShrinkPNG")
if __name__ == "__main__":
    build_gui()
