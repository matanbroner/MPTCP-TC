import socket
from scapy.all import *
from src.protocol import *

MPTCP_CAPABLE = 30

"""
Connection Object
"""
Connection = namedtuple("Connection", ["local_ip", "local_port", "remote_ip", "remote_port"])

"""
Convert Protocol Client
Parameters:
    host [str]: Transport Converter server host
    port [int]: Transport Converter server port
"""
class ConvertClient:
    def __init__(self, tc_host: str, tc_port: int):
        self.tc_host = tc_host
        self.tc_port = tc_port
        self.connections = {}
        
    
    def reroute_connection_to_ts(self, syn_packet: scapy.packet.Packet):
        """
        Initiate a connection to a server through the Transport Converter
        Parameters:
            syn_packet [scapy.packet.Packet]: SYN packet to be sent to the server
        """
        # Modify the dst IP and port of the SYN packet to the Transport Converter
        # Store the original dst IP and port in TLV
        server_ip = syn_packet[IP].dst
        server_port = syn_packet[TCP].dport
        syn_packet[IP].dst = self.tc_host
        syn_packet[TCP].dport = self.tc_port
        
        # # Craft the Connect TLV
        # tlv = ConvertProtocolFixedHeader()
        # connect = ConnectTLV(
        #     remote_peer_port=server_port,
        #     remote_peer_ip=server_ip
        # )
        # connect.set_length()
        # tlv = tlv / connect
        # tlv.set_length()
                
        # # Attach the TLV to the SYN payload as a new TCP packet
        # syn_packet = syn_packet / tlv
        
        # Setup connection in cache
        # We use this to source the port number for incoming packets
        self.connections[(syn_packet[IP].src, syn_packet[TCP].sport)] = Connection(
            local_ip=syn_packet[IP].src,
            local_port=syn_packet[TCP].sport,
            remote_ip=server_ip,
            remote_port=server_port
        )
            
                        
        return syn_packet
        
    def on_packet(self, packet):
        pkt = IP(packet.get_payload())
        payload, modified = None, False
        # if TCP packet
        if TCP in pkt:
            flags = pkt[TCP].flags
            # if SYN packet and came from local machine (ie. not from Transport Converter)
            if flags == 'S':
                payload, modified = self.on_tcp_syn(pkt)
            # if SYN-ACK packet and came from Transport Converter
            elif flags == 'SA':
                payload, modified = self.on_tcp_syn_ack(pkt)
            del pkt[IP].chksum
            del pkt[TCP].chksum
        
        if modified:
            payload.show2()
            packet.drop()
            send(payload, iface="enp0s3")
        else:
            packet.accept()
        
    def on_tcp_syn(self, pkt):
        print("Received SYN packet")
        # if packet is MPTCP capable, send SYN to Transport Converter
        options = pkt[TCP].options
        for option in options:
            if option[0] == MPTCP_CAPABLE:
                    pkt = self.reroute_connection_to_ts(pkt)
                    return pkt, True
        return pkt, False
    
    def on_tcp_syn_ack(self, pkt):
        print("Received SYN-ACK packet")
        # Make sure we have the connection in cache
        if (pkt[IP].dst, pkt[TCP].dport) not in self.connections:
            return pkt, False
        connection = self.connections[(pkt[IP].dst, pkt[TCP].dport)]
        # Modify the src IP and port of the SYN-ACK packet to the original server
        pkt[IP].src = connection.remote_ip
        pkt[TCP].sport = connection.remote_port
        return pkt, True
        