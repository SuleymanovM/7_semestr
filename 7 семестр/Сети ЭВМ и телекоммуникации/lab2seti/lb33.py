import socket
import tkinter as tk
from tkinter import messagebox, font


# Подключение к серверу
def connect_to_server():
    try:
        server_ip = entry_ip.get()
        server_port = int(entry_port.get())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        return client_socket
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к серверу: {e}")
        return None

# Отправка команды на сервер
def send_command():
    command = entry_command.get()
    client_socket = connect_to_server()
    if client_socket:
        client_socket.send(command.encode())  # Отправляем команду на сервер
        response = client_socket.recv(1024)  # Получаем ответ от сервера
        try:
            decoded_response = response.decode('utf-8')
            messagebox.showinfo("Ответ от сервера", decoded_response)
            if command.lower() == 'bye':
                client_socket.close()
                root.quit()
        except UnicodeDecodeError:
            hex_response = response.hex()
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, hex_response)
        finally:
            client_socket.close()

# Основное окно
root = tk.Tk()
root.title("Клиент серверного приложения")
root.geometry("580x400")  # Задаем размер окна
root.configure(bg="#f0f0f0")  # Фоновый цвет окна

# Шрифты
label_font = font.Font(family="Arial", size=12)
entry_font = font.Font(family="Arial", size=10)

# Элементы интерфейса
label_ip = tk.Label(root, text="IP сервера:", bg="#f0f0f0", font=label_font)
label_ip.grid(row=0, column=0, padx=10, pady=10)
entry_ip = tk.Entry(root, font=entry_font, width=60)  # Увеличиваем ширину поля ввода
entry_ip.grid(row=0, column=1, padx=10, pady=10)

label_port = tk.Label(root, text="Порт сервера:", bg="#f0f0f0", font=label_font)
label_port.grid(row=1, column=0, padx=10, pady=10)
entry_port = tk.Entry(root, font=entry_font, width=60)  # Увеличиваем ширину поля ввода
entry_port.grid(row=1, column=1, padx=10, pady=10)

label_command = tk.Label(root, text="Команда:", bg="#f0f0f0", font=label_font)
label_command.grid(row=2, column=0, padx=10, pady=10)
entry_command = tk.Entry(root, font=entry_font, width=60)  # Увеличиваем ширину поля ввода
entry_command.grid(row=2, column=1, padx=10, pady=10)

button_send = tk.Button(root, text="Отправить", command=send_command,
                         bg="#4CAF50", fg="white", font=("Arial", 12), relief=tk.RAISED)
button_send.grid(row=3, column=0, columnspan=2, pady=(10, 20))

# Поле Text для вывода зашифрованных данных
text_output = tk.Text(root, height=10, width=70, bg="#ffffff", font=("Courier New", 10))
text_output.grid(row=4, column=0, columnspan=2)

# Запуск основного цикла приложения
root.mainloop()


