import pandas as pd
from datetime import datetime

import client_socket_API
import server_socket_API

while True:

    server_socket_API.init()
    server_socket_API.set_to_listen()
    message = server_socket_API.get_message()
    print(message)
    SEPARATOR = ','
    message_split = message.split(SEPARATOR)

    date_time_obj = datetime.strptime(message_split[1], '%Y-%m-%d_%H-%M-%S')

    initial_data = {
        'RFID': [message_split[0]]
        , 'DATE_TIME_READ': [date_time_obj]
    }

    data_df = pd.DataFrame.from_dict(initial_data,)

    # TODO: Classification
    classified_black = 1
    classified_white = 1
    classified_green = 1

    data_df['BLACK_BAG'] = classified_black
    data_df['WHITE_BAG'] = classified_white
    data_df['GREEN_BAG'] = classified_green

    # TODO: Send to Big Data

    ok_event = input('OK (enter): ')
    client_socket_API.init()
    client_socket_API.establish_connection('192.168.20.23',)
    client_socket_API.send_message_and_close('OK',)









