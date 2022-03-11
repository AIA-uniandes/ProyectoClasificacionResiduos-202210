from datetime import datetime

import client_socket_API
import server_socket_API
# Programa que debe correr el que esta conectado a la antena
while True:
    # Recibir input de la antena
    input_RFID_tag = input('*Put RFID tag between the antenna, This is the TAG READ: ')

    # Tomar la fecha y hora en que fue recibido el tag
    now = datetime.now()
    dt_format = "%Y-%m-%d_%H-%M-%S"
    dt_string = now.strftime(dt_format)

    # Crear mensaje para que pueda ser leido por el servidor (Nano)
    SEPARATOR = ','
    message_to_edge_node = input_RFID_tag + SEPARATOR + dt_string

    # Establecer conexion con nano
    client_socket_API.init()
    client_socket_API.establish_connection('157.253.231.90', 80)
    client_socket_API.send_message_and_close(message_to_edge_node,)

    # Esperar confirmacion de que se puede continuar
    server_socket_API.init()
    server_socket_API.set_to_listen(server_port=5001)
    IP_address, message = server_socket_API.get_message()

    if message == 'OK':
        continue
    else:
        break



