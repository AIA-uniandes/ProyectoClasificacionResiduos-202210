from subprocess import run, PIPE


def get_stdout_from_bash(bash_script):
    out = run([bash_script], shell=True, stdout=PIPE, stderr=PIPE)
    print(out.stderr)
    print(out.stdout)

    var_out = out.stdout.decode('ascii')

    return var_out
