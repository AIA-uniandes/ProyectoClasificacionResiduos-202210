import paramiko

host = "157.253.228.50"

port = 22

username = "ftc"

password = ""

command = "ls"


ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command(command)

lines = stdout.readlines()

print(lines)