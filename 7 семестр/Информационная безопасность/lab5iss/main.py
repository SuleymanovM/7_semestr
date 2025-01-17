import tkinter as tk
from tkinter import filedialog, messagebox
import random
from math import gcd

# Тест Лемана
def is_prime_lehman(n, k=40):
    if n < 2:  # Число меньше 2 — оно не простое.
        return False
    if n in (2, 3):  # Числа 2 и 3 — простые.
        return True
    if n % 2 == 0:  # Если число чётное и не 2, то оно составное.
        return False

    for _ in range(k):  # Повторяем тест k раз для повышения надёжности.
        a = random.randint(2, n - 1)  # Выбираем случайное число a от 2 до n-1.
        if gcd(a, n) != 1:  # Проверяем, что a и n взаимно просты.
            return False  # Если a и n не взаимно просты, то n составное.
        if pow(a, (n - 1) // 2, n) not in (1, n - 1):  # Проверяем условие Лемана.
            return False  # Если условие не выполняется, n составное.

    return True  # Если все проверки прошли, то n, скорее всего, простое.

def generate_prime(start):
    while True:
        if is_prime_lehman(start):  # Проверка, является ли число простым.
            return start  # Если простое, возвращаем его.
        start += 1  # Если нет, пробуем следующее число.


# Генерация ключей RSA
def generate_rsa_keys():
    # Генерация простых чисел p и q
    p = generate_prime(random.randint(1000000000, 3000000000))
    q = generate_prime(random.randint(1000000000, 3000000000))
    n = p * q
    m = (p - 1) * (q - 1)

    # Выбор e
    d = random.randint(2, m - 1)
    while gcd(d, m) != 1:
        d = random.randint(2, m - 1)

    # Вычисление d
    e = pow(d, -1, m)

    return (d, n), (e, n)  # Открытый и закрытый ключи

# Шифрование
def rsa_encrypt(message, public_key):   #Принимает сообщение и открытый ключ.
    e, n = public_key   #Для каждого байта сообщения вычисляет pow(byte, e, n), что соответствует шифрованию.
    return [pow(byte, e, n) for byte in message]    #Возвращает зашифрованное сообщение в виде списка целых чисел.

# Дешифрование
def rsa_decrypt(encrypted_message, private_key):    #Принимает зашифрованное сообщение и закрытый ключ.
    d, n = private_key      #Дешифрует каждый байт, вычисляя pow(byte, d, n).
    return bytes([pow(byte, d, n) for byte in encrypted_message])       #Возвращает расшифрованные данные в формате байтов.


# --- GUI приложение ---
class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Шифрование")

        # Переменные
        self.public_key = None
        self.private_key = None

        # Элементы интерфейса
        self.button_generate_keys = tk.Button(root, text="Сгенерировать ключи", command=self.generate_keys)
        self.button_generate_keys.pack()

        self.label_keys = tk.Label(root, text="Открытый и закрытый ключи:")
        self.label_keys.pack()

        self.button_encrypt = tk.Button(root, text="Зашифровать файл", command=self.encrypt_file)
        self.button_encrypt.pack()

        self.button_decrypt = tk.Button(root, text="Дешифровать файл", command=self.decrypt_file)
        self.button_decrypt.pack()

    def generate_keys(self):
        self.public_key, self.private_key = generate_rsa_keys()
        self.label_keys.config(
            text=f"Открытый ключ: {self.public_key}\nЗакрытый ключ: {self.private_key}"
        )

    def encrypt_file(self): #Проверяет, сгенерированы ли ключи, и предлагает пользователю выбрать файл для шифрования.
        if not self.public_key:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        file_path = filedialog.askopenfilename()
        if file_path: #Шифрует содержимое файла и предлагает сохранить зашифрованные данные в новом файле.
            with open(file_path, "rb") as file:
                data = file.read()
            encrypted_data = rsa_encrypt(data, self.public_key)
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(save_path, "w") as file:
                file.write(" ".join(map(str, encrypted_data)))
            messagebox.showinfo("Успех", "Файл успешно зашифрован")

    def decrypt_file(self):
        if not self.private_key:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                encrypted_data = list(map(int, file.read().split()))
            decrypted_data = rsa_decrypt(encrypted_data, self.private_key)
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(save_path, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Успех", "Файл успешно расшифрован")


root = tk.Tk()
app = RSAApp(root)
root.mainloop()
