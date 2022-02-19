from datetime import datetime

import client_socket_API
import server_socket_API

while True:
    input_RFID_tag = input('*Put RFID tag between the antenna, This is the TAG READ: ')

    now = datetime.now()
    dt_format = "%Y-%m-%d_%H-%M-%S"
    dt_string = now.strftime(dt_format)

    SEPARATOR = ','
    message_to_edge_node = input_RFID_tag + SEPARATOR + dt_string

    client_socket_API.init()
    client_socket_API.establish_connection('192.168.20.87',)
    client_socket_API.send_message_and_close(message_to_edge_node,)

    server_socket_API.init()
    server_socket_API.set_to_listen()
    IP_address, message = server_socket_API.get_message()

    if message == 'OK':
        continue
    else:
        break



