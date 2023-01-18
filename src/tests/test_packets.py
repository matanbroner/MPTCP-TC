from scapy.all import *
from src.client import ConvertClient

def tcp_packet():
    return IP(dst='1.2.3.4') / TCP(dport=80)

def test_connect():
    client = ConvertClient('127.0.0.1', 8080)
    client.connect(tcp_packet())
    
test_connect()