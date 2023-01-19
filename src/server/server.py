import socket
import threading
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
        
        # Run TCP server to listen for incoming connections from the client
        # In a separate thread
        t = threading.Thread(target=self.run_tcp_server)
        t.start()
        t.join()
        
    
    def proxy_packet(self, pkt: scapy.packet.Packet):
        """
        Proxy a packet to the server or client
        Maintain a cache of connections
        Parameters:
            pkt [scapy.packet.Packet]: Packet to be proxied
        """
        pass
    
    def run_tcp_server(self):
        """
        Run a TCP server to listen for incoming connections from the client
        """
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.host, self.port)
        sock.bind(server_address)
        sock.listen(1)
        print("Listening on: ", server_address)
        while True:
            connection, client_address = sock.accept()
            print("Connection from: ", client_address)
            try:
                all_data = []
                while True:
                    data = connection.recv(2048)
                    if data:
                        all_data.append(data)
                    else:
                        break
                print("Received: ", all_data)
            finally:
                # Clean up the connection
                connection.close()
        
    def on_packet(self, packet):
        pkt = IP(packet.get_payload())
        pkt.show()
            
        packet.drop()