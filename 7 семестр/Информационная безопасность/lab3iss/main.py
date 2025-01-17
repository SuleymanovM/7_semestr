import tkinter as tk
from tkinter import messagebox
import os
import random

# Таблица sTable (берётся из MaHash7)
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


# Операция циклического сдвига влево
def LROT(x):
    return ((x << 11) | (x >> 21)) & 0xFFFFFFFF #Выполняет циклический сдвиг 32-битного числа x влево на 11 или 21 вправо бит,
                                                # Применяет маску 0xFFFFFFFF, чтобы гарантировать 32-битный результат


# Операция циклического сдвига вправо
def RROT(x):
    return ((x >> 11) | (x << 21)) & 0xFFFFFFFF


# Функция хеширования MaHash4
def MaHash4(input_string):
    input_bytes = input_string.encode('utf-8')  # Кодируем строку в байты (UTF-8)
    hash1 = len(input_bytes)  # Инициализируем первый хеш значением длины строки
    hash2 = len(input_bytes)  # Инициализируем второй хеш значением длины строки

    # Проходим по всем байтам строки
    for i in range(len(input_bytes)):
        byte = input_bytes[i]

        # Первый хеш: изменяется с использованием таблицы sTable и циклического сдвига влево
        hash1 += sTable[(byte + i) & 255]  # Используем байт и его индекс для индексации в sTable
        hash1 = LROT(hash1 + ((hash1 << 6) ^ (hash1 >> 8)))  # Применяем циклический сдвиг и дополнительные операции

        # Второй хеш: изменяется с использованием таблицы sTable и циклического сдвига вправо
        hash2 += sTable[(byte + i) & 255]  # Аналогично для второго хеша
        hash2 = RROT(
            hash2 + ((hash2 << 6) ^ (hash2 >> 8)))  # Применяем циклический сдвиг вправо и дополнительные операции

        # Слияние хешей
        sh1 = hash1
        sh2 = hash2
        hash1 = ((sh1 >> 16) & 0xFFFF) | ((sh2 & 0xFFFF) << 16)  # Объединяем части первого хеша и второго
        hash2 = ((sh2 >> 16) & 0xFFFF) | ((sh1 & 0xFFFF) << 16)  # Объединяем части второго хеша и первого

    return hash1 ^ hash2  # Возвращаем итоговый результат как XOR двух хешей

    return hash1 ^ hash2


# Функция для генерации маски на основе пароля
def generate_mask(password, length):
    hash_value = MaHash4(password)
    return bytes([(hash_value >> (i % 8)) & 0xFF for i in range(length)])


# Потоковое шифрование/дешифрование XOR на основе генератора псевдослучайных чисел
def stream_cipher(data, key, mask):
    return bytes([b ^ key[i % len(key)] ^ mask[i % len(mask)] for i, b in enumerate(data)])
#реализация поточного шифрования с использованием операции XOR.

# Линейный конгруэнтный генератор для генерации псевдослучайной последовательности
def linear_congruential_generator(seed, length):
    a = 1664525          # Множитель
    c = 1013904223       # Приращение
    m = 2 ** 32          # Модуль (максимальное значение, до которого могут доходить числа)
    sequence = []        # Список для хранения последовательности

    x = seed             # Начальное значение (зерно)

    for _ in range(length):
        x = (a * x + c) % m   # Основная формула ЛКГ для генерации следующего числа
        sequence.append(x & 1)  # Берём младший бит (0 или 1) и добавляем в последовательность

    return sequence

# Функция для сохранения последовательности в файл
def save_to_file(sequence, file_path="text.txt"):
    with open(file_path, 'w') as f:
        for bit in sequence:
            f.write(str(bit))
    print(f"Последовательность сохранена в файл {file_path}")


# Функция для генерации и сохранения содержимого файла
def generate_and_save_file():
    try:
        length = 10000
        if length <= 0:
            raise ValueError("Длина должна быть больше 0")

        # Генерация случайной последовательности
        sequence = linear_congruential_generator(random.randint(1, 2 ** 32 - 1), length)

        # Сохранение последовательности в файл
        save_to_file(sequence)

        # Показываем сообщение об успешном завершении
        messagebox.showinfo("Успех", "Файл сгенерирован и сохранён.")
    except ValueError as e:
        # Обработка ошибки, если длина последовательности неправильная
        messagebox.showerror("Ошибка", f"Неверный ввод: {e}")
    except Exception as e:
        # Обработка других ошибок
        messagebox.showerror("Ошибка", f"Не удалось создать файл: {e}")


# Полный путь к исходному файлу
file_path = "text.txt"


# Функция для шифрования файла
def encrypt_file():
    password = entry_password.get()

    if not password:
        messagebox.showerror("Ошибка", "Укажите пароль!")
        return

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        # Хеширование пароля для создания ключа
        key = MaHash4(password).to_bytes(4, 'little')

        # Генерация маски
        mask = generate_mask(password, len(data))

        # Шифруем данные, используя потоковый шифр
        encrypted_data = stream_cipher(data, key, mask)

        # Определяем путь к файлу, в который будет сохранён зашифрованный контент
        save_path = os.path.join(os.path.dirname(file_path), "encrypted_" + os.path.basename(file_path))
        with open(save_path, 'wb') as f:
            f.write(encrypted_data)
        messagebox.showinfo("Успех", f"Файл зашифрован и сохранён как {save_path}.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось зашифровать файл: {e}")


# Функция для дешифрования зашифрованного файла
def decrypt_file():
    password = entry_password.get()

    if not password:
        messagebox.showerror("Ошибка", "Укажите пароль!")
        return

    # Путь к зашифрованному файлу
    encrypted_file_path = os.path.join(os.path.dirname(file_path), "encrypted_" + os.path.basename(file_path))

    try:
        # Открываем зашифрованный файл для чтения в бинарном режиме
        with open(encrypted_file_path, 'rb') as f:
            data = f.read()

        # Хеширование пароля для создания ключа
        key = MaHash4(password).to_bytes(4, 'little')

        # Генерация маски на основе пароля и длины данных
        mask = generate_mask(password, len(data))

        # Дешифруем данные, используя потоковый шифр
        decrypted_data = stream_cipher(data, key, mask)

        save_path = os.path.join(os.path.dirname(file_path), "decrypted_" + os.path.basename(file_path))
        # Открываем файл для записи дешифрованных данных в бинарном режиме
        with open(save_path, 'wb') as f:
            f.write(decrypted_data)     # Записываем дешифрованные данные в новый файл
        messagebox.showinfo("Успех", f"Файл дешифрован и сохранён как {save_path}.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось дешифровать файл: {e}")


# Создание графического интерфейса
root = tk.Tk()
root.title("Шифрование и дешифрование файлов")

# Поле для ввода пароля
label_password = tk.Label(root, text="Пароль:")
label_password.pack()
entry_password = tk.Entry(root, show='*')
entry_password.pack()
button_encrypt = tk.Button(root, text="Зашифровать", command=encrypt_file)
button_encrypt.pack()
button_decrypt = tk.Button(root, text="Дешифровать", command=decrypt_file)
button_decrypt.pack()

# Запуск графического интерфейса
root.mainloop()
