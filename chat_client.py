import cryptocode
import socket
import threading

target_host = "127.0.0.1"
target_port = 8888

def main():
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create connection
    client.connect((target_host, target_port))
    # prepare thread for broadcasts
    chat_handler = threading.Thread(target=handle_chat, args=(client,))
    chat_handler.start()
    # prepare thread to accept user input dans send it to server
    input_handler = threading.Thread(target=handle_input, args=(client,))
    input_handler.start()

def handle_input(sock):
    while True:
        message = input("")
        crypted = cryptocode.encrypt(message, "password123")
        sock.send(str(crypted).encode())


def handle_chat(sock):
    while True:
        data = sock.recv(4096)
        messages = str(data.decode())
        decrypted = cryptocode.decrypt(messages, "password123")
        print(str(decrypted))

    
if __name__ == "__main__":
    main()
