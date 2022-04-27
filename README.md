# AIA-robot-project

## Prerequisites

### Prepare All Hardware

1. Ensure that the RFID server is on and connected to the Antenna. 
2. Turn on the Nano Jetson and connect it to a Camera. The Nano Jetson also has to be connected via LAN to a local network.
3. Make sure the Robot is turned on and has an available IP.
4. Turn on the band mechanism with the OneStopUltrasound.py code.

### Prepare Communication

All of the different devices should be connected under the same network. 

1. On the RFID code (RFID_module_communication.py): Modify the IP on line 21.
2. On the Nano Jetson code (nano_jetson_final_integration.py): Modify the robot_ip on line 29 and the bands_txt_controller_ip on line 40.

## Execution

### Start Up the Services

Please start up in the order that they are listed: 

1. Make sure the RFID server is running and the cursor is placed on the terminal. 
This can be achieved by either running "python PATH_TO_REPO/communication_trials/RFID_module_communication.py" via a terminal (cursor is already placed for input) 
or, if the program is running in an IDE, you have to mannualy place the cursor on the terminal.
2. Ensure the Docker Container on the Nano Jetson is running. For this you have open up a terminal on the Nano, cd into 'jetson-inference/' and run 'sudo docker/run_perisist_detection_dir.sh'. (This has to be done exactly as stated, the docker bash won't run if you cd into the folder that is placed. It has to be run from the parent folder).
3. Run the Nano Jetson server. 'python PATH_TO_REPO/communication_trials/nano_jetson_final_integration.py'.

### Run the entire System

Once everything is ready you can run an RFID tag through the antenna and everything should be working smoothly.

### During the First Execution

BEFORE RUNNING AN RFID TAG THROUGH THE ANTENNA.

As a one time thing for the Bands Controller you have to 'OK' the connection with the Nano. This is done on the visual interface for the first connection only (once the first tag is run through the antenna).













