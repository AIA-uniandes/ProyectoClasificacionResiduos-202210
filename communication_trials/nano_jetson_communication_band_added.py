import sys
from datetime import datetime

import bigquery_comms_API
import client_socket_API
import paramiko_band_movement_API
import server_socket_API

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

repetitive_command_bands = 'apps/151de0c0-965c-11ec-8bc2-0800200c9a66/one_stop_ultrasound.py'
paramiko_band_movement_API.establish_connection(host='', username='', password='',)

while True:

    server_socket_API.init()
    server_socket_API.set_to_listen()
    IP_address, message = server_socket_API.get_message()
    SEPARATOR = ','
    message_split = message.split(SEPARATOR)

    date_time_obj = datetime.strptime(message_split[1], '%Y-%m-%d_%H-%M-%S')

    detected_data = {
        'RFID': message_split[0]
        , 'DATE_REGISTERED': date_time_obj.isoformat()
    }
    
    paramiko_band_movement_API.exec_command_exit_status(command_path=repetitive_command_bands)

    path_to_detected_bags_file = ''
    if sys.platform.startswith('win'):
        print('internal testing')
        path_to_detected_bags_file = 'trial_result.txt'
    else:
        print('nano')
        # TODO: Execute Docker .py & Look for File Result of Classifications
        path_to_detected_bags_file = ''

    file = open(path_to_detected_bags_file, 'rt')
    data = file.read()
    classified_bags = data.split('\n')

    classified_dict = {
        'black': 0
        , 'white': 0
        , 'green': 0
        , 'undefined': 0
    }
    
    peek_first_bag_to_deposit = classified_bags.pop(0)
    classified_dict[peek_first_bag_to_deposit] += 1
    # TODO: Deposit first bag

    for bag_color in classified_bags:
        paramiko_band_movement_API.exec_command(command_path=repetitive_command_bands)
        # TODO: Send command to Robot for Depositing
        classified_dict[bag_color] += 1

    detected_black = dict(detected_data)
    detected_black['BAG_COLOR'] = 'black'
    detected_black['BAG_COUNT'] = classified_dict['black']

    detected_white = dict(detected_data)
    detected_white['BAG_COLOR'] = 'white'
    detected_white['BAG_COUNT'] = classified_dict['white']

    detected_green = dict(detected_data)
    detected_green['BAG_COLOR'] = 'green'
    detected_green['BAG_COUNT'] = classified_dict['green']

    detected_undefined = dict(detected_data)
    detected_undefined['BAG_COLOR'] = 'undefined'
    detected_undefined['BAG_COUNT'] = classified_dict['undefined']

    detected_rows = []
    if classified_dict['black'] > 0:
        detected_rows.append(detected_black)

    if classified_dict['white'] > 0:
        detected_rows.append(detected_white)

    if classified_dict['green'] > 0:
        detected_rows.append(detected_green)

    if classified_dict['undefined'] > 0:
        detected_rows.append(detected_undefined)

    if len(detected_rows) > 0:
        bigquery_comms_API.try_insert_rows_table(rows=detected_rows)

    client_socket_API.init()
    client_socket_API.establish_connection(IP_address,)
    client_socket_API.send_message_and_close('OK',)

