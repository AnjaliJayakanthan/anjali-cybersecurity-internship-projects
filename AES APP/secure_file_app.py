from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

# Generate a single key and save to a file (for demo purposes)
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

fernet = Fernet(load_key())

def encrypt_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    try:
        with open(filepath, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)
        enc_path = filepath + ".enc"
        with open(enc_path, "wb") as enc_file:
            enc_file.write(encrypted)

        messagebox.showinfo("Success", f"🔐 File encrypted and saved as:\n{enc_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")

def decrypt_file():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if not filepath:
        return

    try:
        with open(filepath, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)
        orig_path = filepath.replace(".enc", "_decrypted")

        with open(orig_path, "wb") as dec_file:
            dec_file.write(decrypted)

        messagebox.showinfo("Success", f"🔓 File decrypted and saved as:\n{orig_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")

# GUI setup
root = Tk()
root.title("🔐 Secure File Storage")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#f7f0fa")

title = Label(root, text="Secure File Storage with AES", font=("Helvetica", 14, "bold"), bg="#f7f0fa", fg="#5f4b8b")
title.pack(pady=20)

encrypt_btn = Button(root, text="🔐 Encrypt a File", command=encrypt_file, width=25, bg="#a29bfe", fg="white", font=("Segoe UI", 10, "bold"))
encrypt_btn.pack(pady=10)

decrypt_btn = Button(root, text="🔓 Decrypt a File", command=decrypt_file, width=25, bg="#74b9ff", fg="white", font=("Segoe UI", 10, "bold"))
decrypt_btn.pack(pady=10)

root.mainloop()
