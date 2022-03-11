import sys
from datetime import datetime

import bigquery_comms_API
import client_socket_API
import paramiko_band_movement_API
import robot_movement_API
import server_socket_API
import docker_controller_API

# Acceso a credenciales para conectar en BigQuery
key_management_path = '../API_KEY_MANAGEMENT/'
json_key_file = 'aia-thesis-project-v1-a69cdd9b9882.json'
# Definicion de esquema
schema = [
    {'name': 'RFID', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COLOR', 'type': 'STRING', 'mode': 'required'},
    {'name': 'BAG_COUNT', 'type': 'INTEGER', 'mode': 'required'},
    {'name': 'DATE_REGISTERED', 'type': 'DATETIME', 'mode': 'required'},
]
work_dataset = 'DEVELOPMENT_BETA'
work_table = 'BAG_COUNT_RFID_DATETIME'
# Establecer conexion con BigQuery
bigquery_comms_API.init(key_management_path=key_management_path, json_key_file=json_key_file,
                        work_table=work_table, work_dataset=work_dataset)
# Crear la tabla con el esquema definido si no existe todavia
bigquery_comms_API.create_if_not_exists_table(schema=schema)

robot_ip = '157.253.197.27'

docker_id = ''
if not(sys.platform.startswith('win')):
    # Averiguar el id del contenedor de Docker para mandarle comando
    docker_info = docker_controller_API.get_stdout_from_bash('sudo docker ps')
    info_components = docker_info.split('\n')
    first_space = info_components[1].find(' ')
    docker_id = info_components[1][:first_space]
    print('This is the running docker id: ', docker_id)

bands_txt_controller_ip = '157.253.228.43'
repetitive_command_bands = 'apps/151de0c0-965c-11ec-8bc2-0800200c9a66/one_stop_ultrasound.py'
# Establecer conexion con las bandas
paramiko_band_movement_API.establish_connection(host=bands_txt_controller_ip,)

while True:

    # Preparar la comunicacion
    server_socket_API.init()
    server_socket_API.set_to_listen(server_port=80)
    # Leer Mensaje Escuchado
    IP_address, message = server_socket_API.get_message()
    SEPARATOR = ','
    # Separar Mensaje
    message_split = message.split(SEPARATOR)

    date_time_obj = datetime.strptime(message_split[1], '%Y-%m-%d_%H-%M-%S')
    # Inicializar Diccionario Base
    detected_data = {
        'RFID': message_split[0],
        'DATE_REGISTERED': date_time_obj.isoformat()
    }
    # Ejecutar via SSH comando de las bandas
    # Posicionar la primera bolsa en el ultrasonido para la captura de la imagen
    paramiko_band_movement_API.exec_command_exit_status(command_path=repetitive_command_bands)

    path_to_detected_bags_file = ''
    # Diferenciacion entre pruebas locales y despliegue en el servidor Linux
    if sys.platform.startswith('win'):
        print('internal testing')
        path_to_detected_bags_file = 'trial_result.txt'
    else:
        print('nano')
        # Ejecutar Subproceso para correr Contenedor de Docker
        # El codigo en Docker Carga el modelo de Deteccion, Captura la imagen, Detecta cuantas bolsas, de que color hay
        # Organizados de acuerdo a la proximidad al ultrasonido
        # Al final: escribir resultado en un archivo de directorio compartido (Docker y Nano)
        docker_controller_API.get_stdout_from_bash('sudo docker exec ' + docker_id +
                                                   ' python3 /jetson-inference/data/inside_docker_container.py')
        # Path de Espacio Compartido para leer resultado
        path_to_docker_results = '/home/jetson-inference/data/'
        path_to_detected_bags_file = path_to_docker_results + 'bags_trial.txt'
    # Leer Resultado y convertir a arreglo
    file = open(path_to_detected_bags_file, 'rt')
    data = file.read()
    classified_bags = data.split('\n')
    print(classified_bags)
    # Inicializar diccionario auxiliar para hacer el conteo de las bolsas de cada color
    classified_dict = {
        'black': 0,
        'white': 0,
        'green': 0,
        'undefined': 0
    }
    # Establecer la conexion con el robot
    robot_movement_API.establish_connection_init_parameters(robot_ip)

    # Recoger primera bolsa que ya esta en posicion
    peek_first_bag_to_deposit = classified_bags.pop(0)
    # Agregar al conteo
    classified_dict[peek_first_bag_to_deposit] += 1
    # Enviar comando al robot de depositar
    robot_movement_API.dispose_bag(peek_first_bag_to_deposit)

    # Por cada bolsa que me falta por recoger hacer
    for bag_color in classified_bags:
        print(bag_color)
        # Mover las bandas hasta que se detecte algo
        paramiko_band_movement_API.exec_command_exit_status(command_path=repetitive_command_bands)
        # Depositar bolsa del color que ya sabemos que viene por resultado del docker
        robot_movement_API.dispose_bag(bag_color)
        # Agregar al conteo
        classified_dict[bag_color] += 1

    # Cerrar conexion con robot
    robot_movement_API.close_robot_connection()

    # Crear diccionario para cada color y poder enviar a BigQuery como filas
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
        # Enviar a BigQuery las filas de cada color que haya tenido 1 o mas bolsas depositadas
        bigquery_comms_API.try_insert_rows_table(rows=detected_rows)

    # Establecer conexion con sistema RFID
    client_socket_API.init()
    client_socket_API.establish_connection(IP_address,)
    # Habilitar RFID para que pueda recibir mas tags
    client_socket_API.send_message_and_close('OK',)

