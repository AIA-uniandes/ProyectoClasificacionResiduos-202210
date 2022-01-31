import socket
import time
import math


# Server creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 31001))
server_socket.listen(5)

HOST = "157.253.197.52"    # The remote host #CHANGE IT
PORT = 30002              # The same port as used by the server
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)  # Obligatory (shorturl.at/gwKQY)
s.connect((HOST, PORT))
s.send(("set_tool_voltage(24)" + "\n").encode("utf8"))


"""
-------------------------------------------------------------------
---------------------- MOVEMENT PARAMETERS ------------------------
-------------------------------------------------------------------
"""

position_base = [0, -90, 0, -90, 0, 0]
position_in_between = [64.18, -65.22, 62.34, -92.28, -91.11, 21.78,]
position_ramp = [64.01, -46.74, 62.18, -108.79, -86.05, 21.87,]
position_black_bag = [11.72, -44.16, 40.45, -89.15, -86.05, 21.87,]
position_white_bag = [-17.93, -57.30, 57.64, -88.65, -86.14, 21.87]
position_green_bag = [-40.80, -56.49, 57.65, -94.6, -86.14, 21.87]

bag_dict = {
    'black': position_black_bag
    , 'white': position_white_bag
    , 'green': position_green_bag
}


"""
-------------------------------------------------------------------
------------------------ MOVEMENT BASICS --------------------------
-------------------------------------------------------------------
"""


def move_to_position(array_pos: list,):
    radians_array = convert_arr_to_radians(array_pos)
    s.send(("movej(" + str(radians_array) + ", a=1.0, v=0.3)" + "\n").encode("utf8"))
    time.sleep(8)


def activate_gripper(close=True):
    s.send(("set_digital_out(8," + str(close) + ")" + "\n").encode("utf8"))
    time.sleep(2)


"""
-------------------------------------------------------------------
---------------------- MOVEMENT SPECIFICS -------------------------
-------------------------------------------------------------------
"""


def move_to_base():
    move_to_position(position_base)


def move_to_in_between():
    move_to_position(position_in_between)


def move_to_ramp():
    move_to_position(position_ramp)


def move_to_bag_color(color: str):
    move_to_position(bag_dict[color])


def dispose_bag(color: str):
    move_to_ramp()
    activate_gripper(close=True)
    move_to_in_between()
    move_to_bag_color(color)
    move_to_in_between()
    move_to_base()
    activate_gripper(close=False)


"""
-------------------------------------------------------------------
---------------------- AUXILIARY FUNCTIONS ------------------------
-------------------------------------------------------------------
"""


def convert_arr_to_radians(array_degrees,):
    new_arr = []

    for i in array_degrees:
        new_arr.append(round(math.radians(i), 2))

    return new_arr
