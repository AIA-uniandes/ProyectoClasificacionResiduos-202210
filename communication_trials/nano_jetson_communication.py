import pandas as pd
from datetime import datetime

import client_socket_API
import server_socket_API

while True:

    server_socket_API.init()
    server_socket_API.set_to_listen()
    IP_address, message = server_socket_API.get_message()
    print(message, ', message recieved by: ', IP_address)
    SEPARATOR = ','
    message_split = message.split(SEPARATOR)

    date_time_obj = datetime.strptime(message_split[1], '%Y-%m-%d_%H-%M-%S')

    detected_data = {
        'RFID': [message_split[0]]
        , 'DATE_REGISTERED': [date_time_obj].isoformat()
    }

    # TODO: Classification
    classified_black = 0
    classified_white = 0
    classified_green = 0

    detected_black = detected_data
    detected_black['BAG_COLOR'] = detected_data['black']
    detected_black['BAG_COUNT'] = classified_black

    detected_white = detected_data
    detected_black['BAG_COLOR'] = detected_data['white']
    detected_white['BAG_COUNT'] = classified_white

    detected_green = detected_data
    detected_black['BAG_COLOR'] = detected_data['greens']
    detected_green['BAG_COUNT'] = classified_green

    detected_rows = [detected_black, detected_white, detected_green]

    # TODO: Send to Big Data

    ok_event = input('OK (enter): ')
    client_socket_API.init()
    client_socket_API.establish_connection(IP_address,)
    client_socket_API.send_message_and_close('OK',)









