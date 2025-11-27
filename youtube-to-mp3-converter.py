import os
import subprocess
from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox

LAST_DIR_FILE = os.path.join(os.path.expanduser("~"), ".yt2mp3_last_dir")

def get_last_dir():
    try:
        with open(LAST_DIR_FILE, "r", encoding="utf-8") as f:
            path = f.read().strip()
            if path and os.path.isdir(path):
                return path
    except Exception:
        pass
    return os.getcwd()

def save_last_dir(path):
    try:
        with open(LAST_DIR_FILE, "w", encoding="utf-8") as f:
            f.write(path)
    except Exception:
        pass

def browse_folder():
    path = filedialog.askdirectory(initialdir=dest_var.get() or os.getcwd())
    if path:
        dest_var.set(path)
        save_last_dir(path)

def download_and_convert():
    url = url_var.get().strip()
    dest = dest_var.get().strip()
    if not url:
        messagebox.showwarning("Fel", "Ange en YouTube-länk")
        return
    if not dest:
        messagebox.showwarning("Fel", "Ange en mapp att spara i")
        return
    btn_start.config(state="disabled")
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=dest)
        base, ext = os.path.splitext(out_file)
        mp3_file = base + ".mp3"
        subprocess.run([
            "ffmpeg", "-y", "-i", out_file,
            "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", mp3_file
        ], check=True)
        os.remove(out_file)
        save_last_dir(dest)
        messagebox.showinfo("Klar", f"Sparad: {mp3_file}")
    except Exception as e:
        messagebox.showerror("Fel", str(e))
    finally:
        btn_start.config(state="normal")

root = tk.Tk()
root.title("YouTube → MP3")

tk.Label(root, text="YouTube-länk:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
url_var = tk.StringVar()
tk.Entry(root, textvariable=url_var, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="Spara i mapp:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
dest_var = tk.StringVar(value=get_last_dir())
tk.Entry(root, textvariable=dest_var, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="...", command=browse_folder).grid(row=1, column=2, padx=5, pady=5)

btn_start = tk.Button(root, text="Ladda ner och konvertera", command=download_and_convert)
btn_start.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

root.mainloop()
