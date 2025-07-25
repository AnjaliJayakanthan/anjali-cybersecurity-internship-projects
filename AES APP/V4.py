from tkinter import *
from tkinter import filedialog, messagebox, Canvas
from cryptography.fernet import Fernet
from PIL import Image
import os
import threading
import time

# 🔐 Steganography Functions
def hide_key_in_image(image_path, key, output_path):
    img = Image.open(image_path)
    binary_key = ''.join([format(byte, '08b') for byte in key])
    pixels = img.convert("RGB").getdata()

    new_pixels = []
    key_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if key_index < len(binary_key):
            r = (r & ~1) | int(binary_key[key_index])
            key_index += 1
        if key_index < len(binary_key):
            g = (g & ~1) | int(binary_key[key_index])
            key_index += 1
        if key_index < len(binary_key):
            b = (b & ~1) | int(binary_key[key_index])
            key_index += 1
        new_pixels.append((r, g, b))

    if key_index < len(binary_key):
        raise ValueError("Image not large enough to store the full key.")

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)

def extract_key_from_image(image_path, key_length=44):
    img = Image.open(image_path)
    pixels = img.convert("RGB").getdata()
    binary_key = ''
    bits_needed = key_length * 8

    for pixel in pixels:
        for color in pixel:
            binary_key += str(color & 1)
            if len(binary_key) >= bits_needed:
                break
        if len(binary_key) >= bits_needed:
            break

    bytes_list = [binary_key[i:i+8] for i in range(0, bits_needed, 8)]
    key = bytes([int(b, 2) for b in bytes_list])
    return key

# 🌈 Laser Animation
def flash_laser(color):
    laser = Canvas(root, width=500, height=450, highlightthickness=0, bg=bg_color)
    laser.place(x=0, y=0)
    line = laser.create_rectangle(0, 450, 500, 430, fill=color, width=0)

    def animate():
        for y in range(450, 0, -5):
            laser.coords(line, 0, y, 500, y - 20)
            time.sleep(0.005)
        laser.destroy()

    threading.Thread(target=animate).start()

# 📂 File Encryption
def encrypt_file():
    messagebox.showinfo("Step 1", "🌸 Choose an image that will store your encryption key.")
    image_path = filedialog.askopenfilename(title="Choose Image to Hide Key",filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")],initialdir=os.path.expanduser("~"))
    if not image_path:
        return

    messagebox.showinfo("Step 2", "📁 Now choose the file you want to encrypt.")
    filepath = filedialog.askopenfilename(title="Choose File to Encrypt",initialdir=os.path.expanduser("~"))
    if not filepath:
        return

    try:
        key = Fernet.generate_key()
        fernet = Fernet(key)

        with open(filepath, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)
        enc_path = filepath + ".enc"

        with open(enc_path, "wb") as enc_file:
            enc_file.write(encrypted)

        output_img = os.path.splitext(image_path)[0] + "_with_key.png"
        hide_key_in_image(image_path, key, output_img)

        messagebox.showinfo("Success", f"✨ File encrypted!\nSaved as:\n{enc_path}\n🔑 Key hidden in:\n{output_img}")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")

# 📂 File Decryption
def decrypt_file():
    messagebox.showinfo("Step 1", "🌸 Choose the image that contains your hidden key.")
    image_path = filedialog.askopenfilename(title="Choose Image Containing Hidden Key",filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")],initialdir=os.path.expanduser("~"))
    if not image_path:
        return

    messagebox.showinfo("Step 2", "📁 Now choose the encrypted file you want to decrypt.")
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")],title="Choose File to Decrypt",initialdir=os.path.expanduser("~"))
    if not filepath:
        return

    try:
        key = extract_key_from_image(image_path)
        fernet = Fernet(key)

        with open(filepath, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)
        orig_path = filepath.replace(".enc", "_decrypted")

        with open(orig_path, "wb") as dec_file:
            dec_file.write(decrypted)

        flash_laser("#90ee90")  # light green
        messagebox.showinfo("Decryption Success 🌈", f"🟢 Decryption complete! 🎉\nFile saved as:\n{orig_path}")
    except Exception as e:
        flash_laser("#ff6f61")  # coral red
        messagebox.showerror("Decryption Failed 💥", "🔴 Decryption failed!\nInvalid image or mismatched file.")

# 🌸 GUI Setup
bg_color = "#f5e6f8"
btn_color_encrypt = "#d4a5ff"
btn_color_decrypt = "#a5d6ff"
btn_font = ("Segoe UI", 11, "bold")
title_font = ("Lucida Calligraphy", 14, "bold")

root = Tk()
root.title("🌟 StegoSecure File Vault")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg=bg_color)

Label(root, text="✨ StegoSecure: AES + Steganography ✨", font=title_font, bg=bg_color, fg="#6a4c93").pack(pady=30)

Button(root, text="🔐 Encrypt File + Hide Key", command=encrypt_file,
       bg=btn_color_encrypt, fg="white", font=btn_font, relief="groove",
       activebackground="#be9eff", width=32, bd=4).pack(pady=20)

Button(root, text="🔓 Decrypt File Using Image Key", command=decrypt_file,
       bg=btn_color_decrypt, fg="white", font=btn_font, relief="groove",
       activebackground="#7ecbff", width=32, bd=4).pack(pady=10)

Label(root, text="💖 Built with love by Anjali 💖", font=("Segoe UI", 9), bg=bg_color, fg="#999").pack(side="bottom", pady=15)

root.mainloop()
