from tkinter import *
from tkinter import messagebox
import random

# --- Function: Password Strength Analyzer ---
def analyze_password(event=None):
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Oops!", "Please enter a password to analyze 💬🔐")
        return

    strength = "Very Weak 😵"
    suggestion = password

    if len(password) >= 12 and any(c.isdigit() for c in password) and any(c.isupper() for c in password):
        strength = "Strong 💪✨"
    elif len(password) >= 8:
        strength = "Moderate 😐"
    elif len(password) >= 6:
        strength = "Weak 😬"

    # Slightly more secure suggestion
    suggestion = password + random.choice(["@12", "_secure", "!99", "#x"])

    remark_label.config(text=f"📝 Remark: {strength}")
    suggestion_entry.config(state='normal')
    suggestion_entry.delete(0, END)
    suggestion_entry.insert(0, suggestion)
    suggestion_entry.config(state='readonly')

    # Generate new password from input info
    inputs = [fruit_entry.get(), band_entry.get(), flower_entry.get()]
    inputs = [i for i in inputs if i]
    if inputs:
        base = random.choice(inputs)
        new_pass = base.capitalize() + random.choice(["@123", "2025!", "_pro", "!xX"])
        newpass_entry.config(state='normal')
        newpass_entry.delete(0, END)
        newpass_entry.insert(0, new_pass)
        newpass_entry.config(state='readonly')

# --- Window Setup ---
root = Tk()
root.title("👑 Anjali's Cyber Tool 💻🎀")
root.geometry("880x560")
root.resizable(False, False)

# --- Gradient Background using Canvas ---
canvas = Canvas(root, width=880, height=560)
canvas.pack(fill="both", expand=True)

for i in range(0, 560):
    red = 255
    green = int(230 + i * 0.04)
    blue = int(240 + i * 0.02)
    hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    canvas.create_line(0, i, 880, i, fill=hex_color)

# --- Frame Overlay on Canvas ---
main_frame = Frame(root, bg="#ffffff", bd=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# --- Title ---
title = Label(canvas, text="👑 ANJALI'S CYBER TOOL 🎀", font=("Lucida Calligraphy", 22, "bold"), bg=canvas["bg"], fg="#c94f7c")
canvas.create_window(440, 30, window=title)

# --- Left & Right Frames ---
left_frame = Frame(canvas, bg="#fff8fb", bd=0, highlightbackground="#ffc0cb", highlightthickness=1)
right_frame = Frame(canvas, bg="#fff8fb", bd=0, highlightbackground="#ffc0cb", highlightthickness=1)

canvas.create_window(220, 300, window=left_frame, width=400, height=460)
canvas.create_window(660, 300, window=right_frame, width=400, height=460)

# --- LEFT SIDE ---
Label(left_frame, text="🧚‍♀️ User Details", font=("Georgia", 14, "bold"), bg="#fff8fb", fg="#8e007f").pack(anchor="w", pady=(10, 5), padx=20)

name_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)
dob_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)
email_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)
fruit_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)
band_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)
flower_entry = Entry(left_frame, font=("Segoe UI", 10), width=30)

fields = [
    ("👩‍💼 Name:", name_entry),
    ("📅 Date of Birth:", dob_entry),
    ("📧 Email ID:", email_entry)
]

for label_text, entry in fields:
    Label(left_frame, text=label_text, font=("Georgia", 11), bg="#fff8fb").pack(anchor="w", padx=20)
    entry.pack(anchor="w", padx=20, pady=2)

Label(left_frame, text="🎀 Generator Info", font=("Georgia", 14, "bold"), bg="#fff8fb", fg="#8e007f").pack(anchor="w", pady=(15, 5), padx=20)

gen_fields = [
    ("🍓 Fruit:", fruit_entry),
    ("🎸 Band:", band_entry),
    ("🌸 Flower:", flower_entry)
]

for label_text, entry in gen_fields:
    Label(left_frame, text=label_text, font=("Georgia", 11), bg="#fff8fb").pack(anchor="w", padx=20)
    entry.pack(anchor="w", padx=20, pady=2)

# --- RIGHT SIDE ---
Label(right_frame, text="🔐 Password Analyzer", font=("Georgia", 14, "bold"), bg="#fff8fb", fg="#8e007f").pack(anchor="w", pady=(10, 5), padx=20)

password_entry = Entry(right_frame, font=("Segoe UI", 10), width=30, show="*")
Label(right_frame, text="✏️ Enter Password:", font=("Georgia", 11), bg="#fff8fb").pack(anchor="w", padx=20)
password_entry.pack(anchor="w", padx=20, pady=2)

analyze_btn = Button(right_frame, text="✨ Analyze ✨", font=("Georgia", 11, "bold"), bg="#c94f7c", fg="white", command=analyze_password)
analyze_btn.pack(pady=10)

remark_label = Label(right_frame, text="📝 Remark: ", font=("Georgia", 11), bg="#fff8fb")
remark_label.pack(anchor="w", padx=20, pady=5)

suggestion_entry = Entry(right_frame, font=("Segoe UI", 10), width=30, state="readonly")
Label(right_frame, text="🔁 Instead:", font=("Georgia", 11, "bold"), bg="#fff8fb").pack(anchor="w", padx=20)
suggestion_entry.pack(anchor="w", padx=20, pady=2)

newpass_entry = Entry(right_frame, font=("Segoe UI", 10), width=30, state="readonly")
Label(right_frame, text="🌟 New Password:", font=("Georgia", 11, "bold"), bg="#fff8fb").pack(anchor="w", padx=20)
newpass_entry.pack(anchor="w", padx=20, pady=2)

# --- Keyboard Navigation (Enter key) ---
name_entry.bind("<Return>", lambda e: dob_entry.focus())
dob_entry.bind("<Return>", lambda e: email_entry.focus())
email_entry.bind("<Return>", lambda e: fruit_entry.focus())
fruit_entry.bind("<Return>", lambda e: band_entry.focus())
band_entry.bind("<Return>", lambda e: flower_entry.focus())
flower_entry.bind("<Return>", lambda e: password_entry.focus())
password_entry.bind("<Return>", analyze_password)

root.mainloop()
