from datetime import datetime

import client_socket_API
import server_socket_API
import bigquery_comms_API

key_management_path = '../API_KEY_MANAGEMENT/'
json_key_file = 'aia-thesis-project-v1-a69cdd9b9882.json'
schema = [
    {'name': 'RFID', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COLOR', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COUNT', 'type': 'INTEGER', 'mode': 'required'},
    {'name': 'DATE_REGISTERED', 'type': 'DATETIME', 'mode': 'required'},
]
work_dataset = 'DEVELOPMENT_BETA'
work_table = 'BAG_COUNT_RFID_DATETIME'
bigquery_comms_API.init(key_management_path=key_management_path, json_key_file=json_key_file
                            , work_table=work_table, work_dataset=work_dataset)
bigquery_comms_API.create_if_not_exists_table(schema=schema)

while True:

    server_socket_API.init()
    server_socket_API.set_to_listen()
    IP_address, message = server_socket_API.get_message()
    print(IP_address)
    print(message, ', message received by: ', IP_address)
    SEPARATOR = ','
    message_split = message.split(SEPARATOR)

    date_time_obj = datetime.strptime(message_split[1], '%Y-%m-%d_%H-%M-%S')

    detected_data = {
        'RFID': message_split[0]
        , 'DATE_REGISTERED': date_time_obj.isoformat()
    }

    # TODO: Classification
    classified_black = 0
    classified_white = 0
    classified_green = 0

    detected_black = dict(detected_data)
    detected_black['BAG_COLOR'] = 'black'
    detected_black['BAG_COUNT'] = classified_black

    detected_white = dict(detected_data)
    detected_white['BAG_COLOR'] = 'white'
    detected_white['BAG_COUNT'] = classified_white

    detected_green = dict(detected_data)
    detected_green['BAG_COLOR'] = 'green'
    detected_green['BAG_COUNT'] = classified_green

    detected_rows = [detected_black, detected_white, detected_green]

    bigquery_comms_API.try_insert_rows_table(rows=detected_rows)
    print('data sent to bigquery', detected_rows)

    client_socket_API.init()
    client_socket_API.establish_connection(IP_address,)
    client_socket_API.send_message_and_close('OK',)









