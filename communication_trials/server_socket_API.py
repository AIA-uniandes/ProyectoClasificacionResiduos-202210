import socket

global s


def init():
    global s

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def set_to_listen(server_host='0.0.0.0', server_port=80):
    global s

    s.bind((server_host, server_port))

    s.listen(5)
    print(f"[*] Listening as {server_host}:{server_port}")


def get_message():
    global s

    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    received = client_socket.recv(1024).decode()

    return address[0], received


