import tkinter as tk
from tkinter import messagebox
import os

sTable = [
    0xa3, 0xd7, 0x09, 0x83, 0xf8, 0x48, 0xf6, 0xf4, 0xb3, 0x21, 0x15, 0x78, 0x99, 0xb1, 0xaf, 0xf9,
    0xe7, 0x2d, 0x4d, 0x8a, 0xce, 0x4c, 0xca, 0x2e, 0x52, 0x95, 0xd9, 0x1e, 0x4e, 0x38, 0x44, 0x28,
    0x0a, 0xdf, 0x02, 0xa0, 0x17, 0xf1, 0x60, 0x68, 0x12, 0xb7, 0x7a, 0xc3, 0xe9, 0xfa, 0x3d, 0x53,
    0x96, 0x84, 0x6b, 0xba, 0xf2, 0x63, 0x9a, 0x19, 0x7c, 0xae, 0xe5, 0xf5, 0xf7, 0x16, 0x6a, 0xa2,
    0x39, 0xb6, 0x7b, 0x0f, 0xc1, 0x93, 0x81, 0x1b, 0xee, 0xb4, 0x1a, 0xea, 0xd0, 0x91, 0x2f, 0xb8,
    0x55, 0xb9, 0xda, 0x85, 0x3f, 0x41, 0xbf, 0xe0, 0x5a, 0x58, 0x80, 0x5f, 0x66, 0x0b, 0xd8, 0x90,
    0x35, 0xd5, 0xc0, 0xa7, 0x33, 0x06, 0x65, 0x69, 0x45, 0x00, 0x94, 0x56, 0x6d, 0x98, 0x9b, 0x76,
    0x97, 0xfc, 0xb2, 0xc2, 0xb0, 0xfe, 0xdb, 0x20, 0xe1, 0xeb, 0xd6, 0xe4, 0xdd, 0x47, 0x4a, 0x1d,
    0x42, 0xed, 0x9e, 0x6e, 0x49, 0x3c, 0xcd, 0x43, 0x27, 0xd2, 0x07, 0xd4, 0xde, 0xc7, 0x67, 0x18,
    0x89, 0xcb, 0x30, 0x1f, 0x8d, 0xc6, 0x8f, 0xaa, 0xc8, 0x74, 0xdc, 0xc9, 0x5d, 0x5c, 0x31, 0xa4,
    0x70, 0x88, 0x61, 0x2c, 0x9f, 0x0d, 0x2b, 0x87, 0x50, 0x82, 0x54, 0x64, 0x26, 0x7d, 0x03, 0x40,
    0x34, 0x4b, 0x1c, 0x73, 0xd1, 0xc4, 0xfd, 0x3b, 0xcc, 0xfb, 0x7f, 0xab, 0xe6, 0x3e, 0x5b, 0xa5,
    0xad, 0x04, 0x23, 0x9c, 0x14, 0x51, 0x22, 0xf0, 0x29, 0x79, 0x71, 0x7e, 0xff, 0x8c, 0x0e, 0xe2,
    0x0c, 0xef, 0xbc, 0x72, 0x75, 0x6f, 0x37, 0xa1, 0xec, 0xd3, 0x8e, 0x62, 0x8b, 0x86, 0x10, 0xe8,
    0x08, 0x77, 0x11, 0xbe, 0x92, 0x4f, 0x24, 0xc5, 0x32, 0x36, 0x9d, 0xcf, 0xf3, 0xa6, 0xbb, 0xac,
    0x5e, 0x6c, 0xa9, 0x13, 0x57, 0x25, 0xb5, 0xe3, 0xbd, 0xa8, 0x3a, 0x01, 0x05, 0x59, 0x2a, 0x46
]

# Таблица замены S-блоков ГОСТ 28147-89
S_BOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
]

def maHash3(password):
    # Преобразуем пароль в байты
    data = password.encode('utf-8')
    hash_value = [0x0] * 8  # Инициализируем хэш на 8 блоков

    for byte in data:
        for i in range(8):
            # Используем sTable для изменения каждого блока хэша
            index = (hash_value[i] ^ byte) & 0xFF  # Индекс в таблице sTable
            hash_value[i] = sTable[index]

    # Объединяем блоки в единую хэш-строку
    result = b"".join(h.to_bytes(1, 'little') for h in hash_value)
    return result.ljust(32, b'\0')  # Возвращаем 32 байта



def gost_encrypt_block(block, key):
    n1 = int.from_bytes(block[:4], 'little') #берет первые 4 байта блока и преобразует их в целое число n1.
    n2 = int.from_bytes(block[4:], 'little')

    # 24 раунда прямого шифрования
    for i in range(24):
        n1, n2 = n2 ^ gost_f(n1, key[i % 8]), n1

    # 8 раундов обратных
    for i in range(8):
        n1, n2 = n2 ^ gost_f(n1, key[7 - i]), n1

    return n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

# Простейший алгоритм ГОСТ 28147-89: дешифрование блока
def gost_decrypt_block(block, key):
    n1 = int.from_bytes(block[:4], 'little')
    n2 = int.from_bytes(block[4:], 'little')

    # 8 раундов прямых
    for i in range(8):
        n1, n2 = n2 ^ gost_f(n1, key[i]), n1

    # 24 раунда обратных
    for i in range(24):
        n1, n2 = n2 ^ gost_f(n1, key[(7 - i) % 8]), n1

    return n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

# Функция F из ГОСТ 28147-89
def gost_f(data, key):
    x = (data + key) % (2 ** 32)  # Шаг 1: Сложение данных и ключа (побитовое сложение).
    result = 0  # Инициализация результата.
    for i in range(8):  # Шаг 2: Применение S-блоков.
        result |= S_BOX[i][(x >> (4 * i)) & 0xF] << (4 * i)  # Применяем S-блок для каждого 4-битного сегмента.
    return ((result << 11) & 0xFFFFFFFF) | (result >> 21)  # Шаг 3: Циклический сдвиг и обрезка результата.


# Режим OFB для шифрования/дешифрования
def ofb_process(data, key, iv, encrypt_block_func):
    output = b""  # Инициализируем выходной байт.
    current_iv = iv  # Начальное значение (вектор инициализации) присваивается текущему IV.

    for i in range(0, len(data), 8):  # Проходим через данные, считывая по 8 байт за раз.
        current_iv = encrypt_block_func(current_iv, key)  # Шифруем текущий IV, чтобы получить новую последовательность.
        block = data[i:i + 8]  # Получаем текущий блок данных.

        # Шифруем блок, применяя операцию XOR с текущим IV.
        output += bytes(a ^ b for a, b in zip(block, current_iv[:len(block)]))

    return output  # Возвращаем зашифрованные данные.


# Генерация ключа из пароля
def hash_password(password):
    return maHash3(password)

# Шифрование файла
def encrypt_file():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Ошибка", "Укажите пароль!")
        return

    file_path = "./text.txt"
    if not os.path.exists(file_path):
        messagebox.showerror("Ошибка", "Файл test.txt не найден!")
        return

    try:
        key = [int.from_bytes(hash_password(password)[i:i+4], 'little') for i in range(0, 32, 4)]  # Разбиваем на 8 блоков по 4 байта
        iv = os.urandom(8)  # Случайный вектор инициализации

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = ofb_process(data, key, iv, gost_encrypt_block)

        save_path = "./encrypted_test.txt"
        with open(save_path, 'wb') as f:
            f.write(iv + encrypted_data)  # Сохраняем IV + зашифрованные данные

        messagebox.showinfo("Успех", f"Файл зашифрован как {save_path}.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось зашифровать файл: {e}")

# Дешифрование файла
def decrypt_file():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Ошибка", "Укажите пароль!")
        return

    file_path = "./encrypted_test.txt"
    if not os.path.exists(file_path):
        messagebox.showerror("Ошибка", "Зашифрованный файл не найден!")
        return

    try:
        key = [int.from_bytes(hash_password(password)[i:i+4], 'little') for i in range(0, 32, 4)]  # Разбиваем на 8 блоков по 4 байта

        with open(file_path, 'rb') as f:
            iv = f.read(8)  # Читаем IV
            encrypted_data = f.read()

        decrypted_data = ofb_process(encrypted_data, key, iv, gost_encrypt_block)  # Шифрование и дешифрование симметрично в OFB

        save_path = "./decrypted_text.txt"
        with open(save_path, 'wb') as f:
            f.write(decrypted_data)

        messagebox.showinfo("Успех", f"Файл дешифрован как {save_path}.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось дешифровать файл: {e}")

# Интерфейс
root = tk.Tk()
root.title("Шифрование и дешифрование файлов")

label_password = tk.Label(root, text="Пароль:")
label_password.pack()
entry_password = tk.Entry(root, show='*')
entry_password.pack()

button_encrypt = tk.Button(root, text="Зашифровать", command=encrypt_file)
button_encrypt.pack()

button_decrypt = tk.Button(root, text="Дешифровать", command=decrypt_file)
button_decrypt.pack()

root.mainloop()
