"""
TCP Proxy Server
Uses Scapy to listen for incoming TCP packets and
forwards them to the nested host and port based on the Convert Protocol TLV
"""

import socket
from scapy.all import *

class TCPProxy:
    def __init__(self, port, on_packet):
        self.port = port
        self.client_on_packet = on_packet
        self.connections = {}
        
        sniff(filter="tcp", iface="enp0s8", prn=self.on_packet)
        
    def on_packet(self, packet: scapy.packet.Packet):
        if packet[TCP].dport == self.port:
            print(f"IP: {packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")
            self.client_on_packet(packet)
        
        