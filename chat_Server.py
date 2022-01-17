import socket
import threading
import cryptocode

# create socket
ip = "127.0.0.1"
port = 8888
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
# socket list
conns = []

def main():
    #listen
    server.listen(5)
    print(f"[*] Listening on {ip}:{port}")


    #receive connections
    while True:
        client, address = server.accept()
        # add socket to list
        conns.append(client)
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        # send to thread
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(sock):
    # welcome message
    mess = "Welcome. Enter your name please: "
    crypted_mess = cryptocode.encrypt(mess, "password123")
    sock.send(crypted_mess.encode())
    # user replies with username and bot announces it.
    name = sock.recv(4096)
    named = name.decode()
    decrypted_name = cryptocode.decrypt(named, "password123")
    reply = (f"{decrypted_name} joined the chat")
    print(reply)
    crypted_reply = cryptocode.encrypt(reply, "password123")
    # broadcast loop, every user will see "user joined the chat" when a user joins.
    for i in conns:
        i.send(crypted_reply.encode())
    # while loop to listen and broadcast the chat messages
    while True:
        try:
            data = sock.recv(4096)
            response = data.decode()
        # user left
        except Exception:
            print(decrypted_name + " left.")
            left = f"{decrypted_name} left."
            crypted_left = cryptocode.encrypt(left, "password123")
            sock.close()
            # broadcast user left
            for i in conns:
                i.send(crypted_left.encode())
            return None

        # if a user sends a message
        if response:
            # decrypt the message
            decrypted_res = cryptocode.decrypt(response, "password123")
            # prepare to encrypt user:message for broadcast
            chat = str(decrypted_name + ":" + str(decrypted_res))
            crypted_chat = cryptocode.encrypt(chat, "password123")
            # duplicate socket list, to prevent users to see own messages twice
            connx = conns.copy()
            # if the current sock is in connx, remove it
            if sock in connx:
                connx.remove(sock)
            # send the message to every other users in the list.
                for i in connx:
                    i.send(crypted_chat.encode())
        else:
            # close the sock and remove it from the list
            sock.close()
            conns.remove(sock)

if __name__ == "__main__":
    main()
