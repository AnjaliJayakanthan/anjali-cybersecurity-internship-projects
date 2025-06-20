from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from PIL import Image
import os

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

def extract_key_from_image(image_path, key_length=44):  # Fernet key is 44 characters
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

# 📂 File Encryption
def encrypt_file():
    image_path = filedialog.askopenfilename(title="Choose Image to Hide Key")
    if not image_path:
        return

    filepath = filedialog.askopenfilename(title="Choose File to Encrypt")
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

        messagebox.showinfo("Success", f"🔐 File encrypted!\nSaved as:\n{enc_path}\n\n🔑 Key hidden in:\n{output_img}")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")

# 📂 File Decryption
def decrypt_file():
    image_path = filedialog.askopenfilename(title="Choose Image That Has the Key")
    if not image_path:
        return

    filepath = filedialog.askopenfilename(title="Choose File to Decrypt", filetypes=[("Encrypted Files", "*.enc")])
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

        messagebox.showinfo("Success", f"🔓 File decrypted and saved as:\n{orig_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")

# 🌸 GUI Setup
root = Tk()
root.title("🔐 StegoSecure File Storage")
root.geometry("430x300")
root.resizable(False, False)
root.configure(bg="#f8f0fc")

Label(root, text="StegoSecure: AES + Steganography", font=("Helvetica", 14, "bold"), bg="#f8f0fc", fg="#8e44ad").pack(pady=25)

Button(root, text="🔐 Encrypt File + Hide Key in Image", command=encrypt_file, bg="#a29bfe", fg="white", font=("Segoe UI", 10, "bold"), width=30).pack(pady=15)
Button(root, text="🔓 Decrypt File Using Image Key", command=decrypt_file, bg="#74b9ff", fg="white", font=("Segoe UI", 10, "bold"), width=30).pack(pady=15)

root.mainloop()
