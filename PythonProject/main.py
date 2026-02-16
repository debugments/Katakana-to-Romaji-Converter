# Modern Katakana → Romaji GUI (romkan2 + tkinter)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from romkan2 import to_hepburn

# ---------- THEMES ----------
LIGHT = {
    "bg": "#0f172a",
    "card": "#111827",
    "text": "#e5e7eb",
    "muted": "#9ca3af",
    "accent": "#818cf8",
    "entry": "#1f2933",
    "border": "#374151"
}

DARK = {
    "bg": "#f3f4f6",
    "card": "#ffffff",
    "text": "#111827",
    "muted": "#6b7280",
    "accent": "#6366f1",
    "entry": "#f9fafb",
    "border": "#e5e7eb"
}

theme = LIGHT

root = tk.Tk()
root.withdraw()
katakana_entry = tk.Entry(root)
romaji_entry = tk.Entry(root)

# ---------- FUNCTIONS ----------
def apply_theme():
    root.configure(bg=theme["bg"])

    # Card + labels
    card.configure(bg=theme["card"], highlightbackground=theme["border"])
    title.configure(bg=theme["card"], fg=theme["text"])
    subtitle.configure(bg=theme["card"], fg=theme["muted"])

    # Input box
    input_box.configure(
        bg=theme["entry"],
        fg=theme["text"],
        insertbackground=theme["text"]
    )

    # Output
    output_entry.configure(
        bg=theme["entry"],
        fg=theme["text"]
    )

    # Button container
    btn_frame.configure(bg=theme["card"])

    # Buttons (IMPORTANT FIX)
    for btn in [btn_copy, btn_clear, btn_save, btn_theme]:
        btn.configure(
            bg=theme["accent"],
            fg="white",
            activebackground=theme["accent"],
            activeforeground="white"
        )

    # Footer
    footer.configure(bg=theme["bg"], fg=theme["muted"])

def toggle_theme():
    global theme
    theme = DARK if theme == LIGHT else LIGHT
    apply_theme()

def convert_live(event=None):
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        output_var.set("")
        return
    try:
        output_var.set(to_hepburn(text))
    except:
        output_var.set("")

def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_var.get())

def clear_all():
    input_box.delete("1.0", tk.END)
    output_var.set("")

def save_as_txt():
    katakana_text = katakana_entry.get()
    romaji_text = romaji_entry.get()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save translation"
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{katakana_text} -> {romaji_text}\n")

# ---------- WINDOW ----------
root = tk.Tk()
root.title("Katakana → Romaji Converter")
root.geometry("620x480")
root.resizable(False, False)

# ---------- CARD CONTAINER ----------
card = tk.Frame(root, bd=0, highlightthickness=1)
card.pack(padx=20, pady=20, fill="both", expand=True)

# ---------- HEADER ----------
title = tk.Label(card, text="Katakana → Romaji", font=("Segoe UI", 18, "bold"))
title.pack(anchor="w", padx=20, pady=(20, 0))

subtitle = tk.Label(card, text="just add your katakana and get some Romanji :)",
                    font=("Segoe UI", 10))
subtitle.pack(anchor="w", padx=20, pady=(0, 10))

# ---------- INPUT ----------
input_box = tk.Text(card, height=6, font=("Segoe UI", 12), bd=0, relief="flat")
input_box.pack(fill="x", padx=20, pady=(0, 10))
input_box.bind("<KeyRelease>", convert_live)

# ---------- OUTPUT ----------
output_var = tk.StringVar()
output_entry = tk.Entry(card, textvariable=output_var, font=("Segoe UI", 12), bd=0, relief="flat")
output_entry.pack(fill="x", padx=20, pady=(0, 15))

# ---------- BUTTON ROW ----------
btn_frame = tk.Frame(card, bg=theme["card"])
btn_frame.pack(padx=20, pady=10, fill="x")

def make_btn(text, cmd):
    return tk.Button(btn_frame,
                     text=text,
                     command=cmd,
                     bg=theme["accent"],
                     fg="white",
                     activebackground=theme["accent"],
                     relief="flat",
                     font=("Segoe UI", 10, "bold"),
                     padx=10,
                     pady=6)

btn_copy = make_btn("Copy", copy_text)
btn_copy.pack(side="left", padx=5)

btn_clear = make_btn("Clear", clear_all)
btn_clear.pack(side="left", padx=5)

btn_save = make_btn("Save .txt", save_as_txt)
btn_save.pack(side="left", padx=5)

btn_theme = make_btn("Toggle Theme", toggle_theme)
btn_theme.pack(side="right", padx=5)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, radius=12, padding=8, **kwargs):
        super().__init__(parent, highlightthickness=0, bd=0, **kwargs)

        self.command = command
        self.radius = radius
        self.padding = padding
        self.text = text

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        self.draw()

    def draw(self):
        self.delete("all")

        w = self.winfo_reqwidth() + 20
        h = 30

        self.config(width=w, height=h)

        r = self.radius
        self.create_round_rect(2, 2, w-2, h-2, r, fill=theme["accent"], outline="")

        self.create_text(
            w/2, h/2,
            text=self.text,
            fill="white",
            font=("Segoe UI", 10, "bold")
        )

    def create_round_rect(self, x1, y1, x2, y2, r=10, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_hover(self, event):
        self.itemconfig(1, fill=theme["accent"])

    def on_leave(self, event):
        self.itemconfig(1, fill=theme["accent"])

# ---------- FOOTER ----------
footer = tk.Label(root, text="Hope this helps • Powered by AI and Zeke", font=("Segoe UI", 9))
footer.pack(pady=(0, 10))

# apply theme initially
apply_theme()

# run app
root.mainloop()