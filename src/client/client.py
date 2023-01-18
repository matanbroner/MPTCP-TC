from scapy.all import *
from src.protocol import *

"""
Convert Protocol Client
Parameters:
    host [str]: Transport Converter server host
    port [int]: Transport Converter server port
"""
class ConvertClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
    
    def connect(self, syn_packet: scapy.packet.Packet):
        """
        Initiate a connection to a server through the Transport Converter
        Parameters:
            syn_packet [scapy.packet.Packet]: SYN packet to be sent to the server
        """
        # Modify the dst IP and port of the SYN packet to the Transport Converter
        # Store the original dst IP and port in TLV
        server_ip = syn_packet[IP].dst
        server_port = syn_packet[TCP].dport
        syn_packet[IP].dst = self.host
        syn_packet[TCP].dport = self.port
        
        # Craft the Connect TLV
        tlv = ConvertProtocolFixedHeader()
        connect = ConnectTLV(
            remote_peer_port=server_port,
            remote_peer_ip=server_ip
        )
        connect.set_length()
        tlv = tlv / connect
        tlv.set_length()
                
        # Attach the TLV to the SYN payload as a new TCP packet
        syn_packet = syn_packet / tlv
                        
        print("Sending SYN packet to Transport Converter")
        syn_packet.show()
        
    def on_packet(self, packet):
        print("Received packet from Transport Converter")
        print(packet)
        