"""
TCP Proxy Server
Uses Scapy to listen for incoming TCP packets and
forwards them to the nested host and port based on the Convert Protocol TLV
"""

import socket
from scapy.all import *

from src.protocol import *

class TCPProxy:
    def __init__(self, port, on_packet):
        self.port = port
        self.client_on_packet = on_packet
        self.connections = {}
        
        sniff(filter="tcp", iface="enp0s8", prn=self.on_packet)
        
    def on_packet(self, packet: scapy.packet.Packet):
        if packet[TCP].dport == self.port:
            print(f"IP: {packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")
            # if initial packet (SYN)
            if packet[TCP].flags == "S":
                # get the nested host and port from the Convert Protocol TLV
                # located in the SYN payload
                # parse the payload as a Convert Protocol TLV
                payload = packet[TCP].payload
                tlv = ConvertProtocolFixedHeader(payload)
                tlv.parse()
            self.client_on_packet(packet)
        
        