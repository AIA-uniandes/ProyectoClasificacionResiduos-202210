import socket

global s


def init():
    global s

    s = socket.socket()


def establish_connection(host, port=5001):
    global s

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")


def send_message_and_close(message_string):
    global s

    print('Sending message')
    s.send(message_string.encode())
    print('Message sent')
    s.close()






