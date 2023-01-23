import socket
import threading
from scapy.all import *
from src.protocol import *

from src.server.proxy import TCPProxy

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
        
        # Run TCP server to listen for incoming connections from the client
        # In a separate thread
        t = threading.Thread(target=self.run_tcp_proxy)
        t.start()
        t.join()
        
    
    def run_tcp_proxy(self):
        """
        Run a TCP proxy server to listen for incoming connections from the client
        """
        self.tcp_proxy = TCPProxy(self.port)
        self.tcp_proxy.run()
    