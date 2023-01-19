import socket
from scapy.all import *
from src.protocol import *

MPTCP_CAPABLE = 30

"""
Connection Object
"""
Connection = namedtuple("Connection", ["local_ip", "local_port", "socket"])

"""
Convert Protocol Server
Parameters:
    host [str]
    port [int]
"""

class TransportConverter:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = {}
        
    
    def proxy_packet(self, pkt: scapy.packet.Packet):
        """
        Proxy a packet to the server or client
        Maintain a cache of connections
        Parameters:
            pkt [scapy.packet.Packet]: Packet to be proxied
        """
        pass
       
        
    def on_packet(self, packet):
        pkt = IP(packet.get_payload())
        pkt.show()
            
        packet.drop()