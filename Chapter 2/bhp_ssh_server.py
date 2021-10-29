import socket
import paramiko
import threading
import sys

# using the server host key from the paramiko demo files
host_key = paramiko.RSAKey(filename="test_rsa.key")

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "root" and password == "toor":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[+] Listening for connection...")
    client, addr = sock.accept()
except Exception as e:
    print(f"[-] Listen failed: {e}")
    sys.exit(1)

print("[+] Got a connection!")

try:
    # noinspection PyTypeChecker
    bh_session = paramiko.Transport(client)
    bh_session.add_server_key(host_key)
    server = Server()
    
    try:
        bh_session.start_server(server=server)
    except paramiko.SSHException:
        print("[-] SSH Negotiation failed")
    
    chan = bh_session.accept(20)
    print("[+] Authenticated!")
    print(chan.recv(1024))
    chan.send("Welcome to bhp_ssh!")

    while True:
        
        try:
            command = input("Enter command: ").strip("\n")
            
            if command != "exit":
                chan.send(command)
                print(chan.recv(1024).decode(errors="ignore") + "\n")
            else:
                chan.send("exit")
                print("Exiting...")
                bh_session.close()
                raise Exception("exit")
        except KeyboardInterrupt:
            bh_session.close()
        except Exception as e:
            print(f"[-] Caught exception: {str(e)}")
            bh_session.close()
finally:
    sys.exit(1)


