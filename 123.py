import tkinter as tk
from tkinter import messagebox
import random
import string
import json

# Константы
MIN_LENGTH = 4
MAX_LENGTH = 32
HISTORY_FILE = 'history.json'

# Глобальная история
history = []

def generate_password():
    length = length_var.get()
    use_digits = digits_var.get()
    use_letters = letters_var.get()
    use_symbols = symbols_var.get()

    # Проверки
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов!")
        return

    if not (use_digits or use_letters or use_symbols):
        messagebox.showerror("Ошибка", "Нужно выбрать хотя бы одну категорию символов!")
        return

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_symbols:
        chars += string.punctuation

    password = ''.join(random.choice(chars) for _ in range(length))
    history.insert(0, password)
    update_history_listbox()
    save_history()

def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for pwd in history:
        history_listbox.insert(tk.END, pwd)

def save_history():
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

def load_history():
    global history
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except Exception:
        history = []
    update_history_listbox()

def on_closing():
    save_history()
    root.destroy()

# --- GUI ---
root = tk.Tk()
root.title("Генератор паролей")

length_var = tk.IntVar(value=8)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False) # по умолчанию можно не включать

tk.Label(root, text="Длина пароля:").pack()
tk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, orient="horizontal", variable=length_var).pack()

tk.Checkbutton(root, text="Цифры", variable=digits_var).pack(anchor='w')
tk.Checkbutton(root, text="Буквы", variable=letters_var).pack(anchor='w')
tk.Checkbutton(root, text="Спецсимволы", variable=symbols_var).pack(anchor='w')

tk.Button(root, text="Сгенерировать", command=generate_password).pack(pady=5)

tk.Label(root, text="История паролей:").pack()
history_listbox = tk.Listbox(root, width=32)
history_listbox.pack(padx=10, pady=5)

load_history()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
