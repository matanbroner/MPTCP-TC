"""
TCP Proxy Server
Uses raw sockets to listen for incoming TCP packets and 
forwards them to the nested host and port based on the Convert Protocol TLV
"""

import socket

class TCPProxy:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = {}
        
        # Create raw socket to listen for incoming TCP packets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        self.socket.bind((self.host, self.port))
        
        # Listen for incoming packets
        self.listen()
        
    def listen(self):
        data = self.socket.recvfrom(65535)
        print(data)
        