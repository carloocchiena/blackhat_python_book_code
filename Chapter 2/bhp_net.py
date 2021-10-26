import sys
import socket
import getopt
import threading
import subprocess

#global var
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def run_command(cmd):
    """runs a command and return the output
    """
    cmd = cmd.strip()

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    return output


