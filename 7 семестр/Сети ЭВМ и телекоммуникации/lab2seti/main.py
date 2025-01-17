import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import os

shutdown_flag = threading.Event()


# Функция для шифрования текста или файла
# Функция для получения ключа
def derive_key_from_password(password):
    # Создает 32-байтовый ключ, применяя хэширование SHA-256 к паролю
    return sha256(password.encode('utf-8')).digest()[:32]  # Возвращаем 32 байта


# Шифрование данных
def encrypt_data(data, password):
    key = derive_key_from_password(password)  # Генерация ключа
    iv = os.urandom(16)  # Случайный IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (b" " * (16 - len(data) % 16))
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted


# Функция для дешифрования данных
def decrypt_data(data, password):
    # Приводим пароль к длине 16, 24 или 32 байта для AES
    key = derive_key_from_password(password)  # Генерация ключа
    iv = data[:16]  # Первые 16 байт — это вектор инициализации (IV)
    encrypted_data = data[16:]  # Остальные байты — это шифротекст
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    # Убираем дополнительные символы, добавленные при шифровании
    return decrypted.rstrip(b" ")  # Удаляем пробелы, добавленные при дополнении


# Обработка запросов от клиента
def handle_client(client_socket, addr):
    print(f"Подключение от {addr}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            command, *args = data.split()

            if command.lower() == 'hello':
                response = f"hello variant {args[0]}"
                client_socket.send(response.encode())

            elif command.lower() == 'bye':
                response = f"bye variant {args[0]}"
                client_socket.send(response.encode())
                shutdown_flag.set()
                break

            elif command.lower() == 'encrypt':
                message = ' '.join(args[:-1])
                password = args[-1]
                encrypted_data = encrypt_data(message.encode(), password)
                client_socket.send(encrypted_data)



            elif command.lower() == 'decrypt':
                encrypted_data = bytes.fromhex(' '.join(args[:-1]))
                password = args[-1]
                decrypted_data = decrypt_data(encrypted_data, password)
                client_socket.send(decrypted_data)

            else:
                client_socket.send("Неизвестная команда.".encode())

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()


# Запуск сервера
def start_server(host='127.0.0.1', port=64321):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создаем TCP-сокет
    server_socket.bind((host, port)) # Привязываем сокет к адресу и порту
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while not shutdown_flag.is_set():  # Проверяем флаг завершения
        try:
            server_socket.settimeout(1)  # Таймаут для проверки флага
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
        except socket.timeout:
            continue  # Возвращаемся в цикл, если таймаут истек

    print("Сервер завершает работу.")
    server_socket.close()


if __name__ == "__main__":
    start_server()
