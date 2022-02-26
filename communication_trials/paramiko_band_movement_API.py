import paramiko


global ssh


def establish_connection(host, username, password="", port=22):
    global ssh

    print('Start BAND Connection')
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, port, username, password)
    print('BAND Connected Successfully')


def exec_command_exit_status(command_path):
    global ssh

    export_path = 'export PYTHONPATH=/opt/ftc'

    compound_command = export_path + '&&' + command_path

    stdin, stdout, stderr = ssh.exec_command(compound_command)

    exit_status = stdout.channel.recv_exit_status()

    return exit_status

