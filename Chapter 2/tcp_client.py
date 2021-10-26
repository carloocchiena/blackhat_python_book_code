import socket 

target_host = "www.google.com"
target_port = 80

#create a socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the client
client.connect((target_host, target_port))

#send data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#receive data
response = client.recv(4096)

print (response)

