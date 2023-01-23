"""
TCP Proxy Server
Uses Scapy to listen for incoming TCP packets and
forwards them to the nested host and port based on the Convert Protocol TLV
"""

import socket
from scapy.all import *

class TCPProxy:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = {}
        
        sniff(filter="tcp", prn=self.on_packet)
        
    
    def on_packet(self, pkt):
        pkt.show()
        