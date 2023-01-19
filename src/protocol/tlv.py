import socket
from scapy.all import *


"""
Convert Protocol Fixed Header
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+---------------+---------------+-------------------------------+
| Version       | Total Length  | Magic Number                  |
+---------------+---------------+-------------------------------+
"""
class ConvertProtocolFixedHeader(Packet):
    name = "Convert Protocol Fixed Header"
    fields_desc = [
        BitField(name="version", default=1, size=8),
        BitField(name="total_length", default=0, size=8),
        BitField(name="magic_number", default=0x2263, size=16)
    ]
    
    def set_length(self):
        self.total_length = len(self) // 4
        # call the set_length method for each TLV
        for tlv in self.payload:
            tlv.set_length()
    

"""
Convert Protocol Info TLV
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+---------------+---------------+-------------------------------+
| Type=0x1      | Length        | Zero                          |
+---------------+---------------+-------------------------------+
"""
class InfoTLV(Packet):
    name = "Info TLV"
    fields_desc = [
        BitField(name="type", default=1, size=8),
        BitField(name="length", default=0, size=8),
        BitField(name="zero", default=0, size=16)
    ]
    
    def set_length(self):
        self.length = len(self) // 4

"""
Convert Protocol Connect TLV
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+---------------+---------------+-------------------------------+
| Type=0xA      | Length        | Remote Peer Port              |
+---------------+---------------+-------------------------------+
|                                                               |
| Remote Peer IP Address (128 bits)                             |
|                                                               |
|                                                               |
+---------------------------------------------------------------+
"""    
class ConnectTLV(Packet):
    name = "Connect TLV"
    fields_desc = [
        ByteField(name="type", default=0xA),
        # The Total Length is the number of 32-bit words, including the header
        ByteField(name="length", default=0),
        ShortField(name="remote_peer_port", default=0),
        IPField(name="remote_peer_ip", default="127.0.0.1")
    ]
    
    def set_length(self):
        self.length = len(self) // 4
    
"""
Convert Protocol Error TLV
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+---------------+---------------+----------------+--------------+
| Type=0x1E     | Length        | Error Code     | Value        |
+---------------+---------------+----------------+--------------+
// ... (optional) Value //
+---------------------------------------------------------------+
"""
class ErrorTLV(Packet):
    name = "Error TLV"
    fields_desc = [
        BitField(name="type", default=0x1E, size=8),
        BitField(name="length", default=None, size=8),
        BitField(name="error_code", default=0, size=8),
        StrLenField(name="value", default="", length_from=lambda pkt: (pkt.length - 1) * 4)
    ]
    
    def set_length(self):
        self.length = len(self) // 4


"""
Error Code Values
"""
UNSUPPORTED_VERSION = 0x00
MALFORMED_MESSAGE = 0x01
UNSUPPORTED_MESSAGE = 0x02
MISSING_COOKIE = 0x03
NOT_AUTHORIZED = 0x20
UNSUPPORTED_TCP_OPTION = 0x21
RESOURCE_EXCEEDED = 0x40
NETWORK_FAILURE = 0x41
CONNECTION_RESET = 0x60
DESTINATION_UNREACHABLE = 0x61