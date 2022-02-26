import socket
import time
import math

global s
global bag_dict
global position_base
global position_in_between
global position_ramp
global position_black_bag
global position_white_bag
global position_green_bag


def establish_connection_init_parameters(ip):
    global s
    global bag_dict
    global position_base
    global position_in_between
    global position_ramp
    global position_black_bag
    global position_white_bag
    global position_green_bag

    position_base = [0, -90, 0, -90, 0, 0]
    position_in_between = [67.53, -57.51, 39.67, -96.92, -91.13, 21.77]
    position_ramp = [66.99, -46.60, 40.79, -83.42, -91.20, 21.77]
    position_black_bag = [13.06, -20.38, -4.58, -60.92, -88.86, 21.77]
    position_white_bag = [-11.88, -20.37, -4.58, -60.92, -88.86, 21.77]
    position_green_bag = [-39.22, -20.37, -4.58, -60.92, -88.86, 21.77]

    bag_dict = {
        'black': position_black_bag
        , 'white': position_white_bag
        , 'green': position_green_bag
        , 'undefined': position_black_bag
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
    _move_to_position(position_base, )


def _move_to_in_between():
    _move_to_position(position_in_between, 2)


def _move_to_ramp():
    _move_to_position(position_ramp, )


def _move_to_bag_color(color):
    _move_to_position(bag_dict[color], 4)


def dispose_bag(color):
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

