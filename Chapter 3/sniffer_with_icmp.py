import socket
import os
import struct
import ctypes

# host to listen on
host = "192.168.0.187"

# the structure has been taken from canonical IP Header definition
# i.e. sites.uclouvain.be/SystInfo/usr/include/netinet/ip.h.html
class IP(ctypes.Structure):
    _fields_= [
        ("ihl",          ctypes.c_ubyte, 4),
        ("version",      ctypes.c_ubyte, 4),
        ("tos",          ctypes.c_ubyte),
        ("len",          ctypes.c_ushort),
        ("id",           ctypes.c_ushort),
        ("offset",       ctypes.c_ushort),
        ("ttl",          ctypes.c_ubyte),
        ("protocol_num", ctypes.c_ubyte),
        ("sum",          ctypes.c_ushort),
        ("src",          ctypes.c_uint32),
        ("dst",          ctypes.c_uint32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        self.socket_buffer = socket_buffer

        # map protocol constats to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17:"UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except IndexError:
            self.protocol = str(self.protocol_num)

class ICMP(ctypes.Structure):
    _fields_= [
        ("type",         ctypes.c_ubyte),
        ("code",         ctypes.c_ubyte),
        ("checksum",     ctypes.c_ushort),
        ("unused",       ctypes.c_ushort),
        ("next_hop_mtu", ctypes.c_ushort)
    ]

    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        self.socket_buffer = socket_buffer

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP # windows OS
else:
    socket_protocol = socket.IPPROTO_ICMP # unix OS

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

# i had trouble with my VM here following along the lesson of the book
# sniffer.bind((host, 0))
# so I was able to made it working forwarding to this port
sniffer.bind(("0.0.0.0", 6677))

# keep IP headers in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# if we're on Windows we need to send IOCTL to send promiscuos mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # read in a single packet
        raw_buffer = sniffer.recvfrom(65535)[0]

        # create IP header from the first 20 bytes of the buffer
        ip_header = IP(raw_buffer[:20])

        print(f"Protocol: {ip_header.protocol}, {ip_header.src_address} -> {ip_header.dst_address}")

        # if it's ICMP we want the details:
        if ip_header.protocol == "ICMP":
            # find where our ICMP packet starts
            offset = ip_header.ihl * 4 
            buf = raw_buffer[offset:offset + ctypes.sizeof(ICMP)]

            # create our ICMP structure
            icmp_header = ICMP(buf)

            print(f"ICMP -> Type: {icmp_header.type}, {icmp_header.code}")

# handle CTRL-C
except KeyboardInterrupt:
    # turn off promiscuos mode if it has been activated
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)