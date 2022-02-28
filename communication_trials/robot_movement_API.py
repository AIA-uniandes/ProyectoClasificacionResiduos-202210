import socket
import time
import math

global s
global bag_dict
global bag_time
global position_base
global position_in_between
global position_ramp


def establish_connection_init_parameters(ip):
    global s
    global bag_dict
    global bag_time
    global position_base
    global position_in_between
    global position_ramp

    position_base = [0, -90, 0, -90, 0, 0]
    position_in_between = [68.05, -48.12, -5.10, -60.56, -93.85, 23.79]
    position_ramp = [68.41, -22.63, -4.31, -61.95, -90.99, 23.79]
    position_black_bag = [11.58, -45.05, -9.10, -58.39, -93.72, 23.79]
    position_white_bag = [-14.03, -44.91, -9.10, -58.39, -93.72, 23.79]
    position_green_bag = [-38.39, -37.73, -9.10, -68.79, -93.72, 23.79]

    bag_dict = {
        'black': position_black_bag
        , 'white': position_white_bag
        , 'green': position_green_bag
        , 'undefined': position_black_bag
    }

    bag_time = {
        'black': 4
        , 'white': 6
        , 'green': 8
        , 'undefined': 4
    }

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 31001))
    server_socket.listen(5)

    host = ip  # The remote host #CHANGE IT
    port = 30002  # The same port as used by the server
    global s
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)  # Obligatory (shorturl.at/gwKQY)
    s.connect((host, port))
    s.send(("set_tool_voltage(24)" + "\n").encode("utf8"))


def _move_to_position(array_pos, ts=6):
    global s
    print(array_pos)
    radians_array = _convert_arr_to_radians(array_pos)
    s.send(("movej(" + str(radians_array) + ", a=1.0, v=0.3)" + "\n").encode("utf8"))
    time.sleep(ts)


def _activate_gripper(close=True):
    global s
    s.send(("set_digital_out(8," + str(close) + ")" + "\n").encode("utf8"))
    time.sleep(1)


"""
-------------------------------------------------------------------
---------------------- MOVEMENT SPECIFICS -------------------------
-------------------------------------------------------------------
"""


def _move_to_base():
    global position_base
    _move_to_position(position_base, 6)


def _move_to_in_between():
    global position_in_between
    _move_to_position(position_in_between, 4)


def _move_to_ramp():
    global position_ramp
    _move_to_position(position_ramp, 8)


def _move_to_bag_color(color):
    global bag_dict
    global bag_time
    print(bag_dict)
    print(bag_dict[color])
    _move_to_position(bag_dict[color], bag_time[color])


def dispose_bag(color):
    print('dispose', color)
    _move_to_ramp()
    _activate_gripper(close=True)
    _move_to_in_between()
    _move_to_bag_color(color)
    _activate_gripper(close=False)
    _move_to_base()


def close_robot_connection():
    global s

    s.close()


"""
-------------------------------------------------------------------
---------------------- AUXILIARY FUNCTIONS ------------------------
-------------------------------------------------------------------
"""


def _convert_arr_to_radians(array_degrees, ):
    new_arr = []

    for i in array_degrees:
        new_arr.append(round(math.radians(i), 2))

    return new_arr


