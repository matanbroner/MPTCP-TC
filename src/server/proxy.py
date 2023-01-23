"""
TCP Proxy Server
"""

import socket
import select
import sys

class TCPProxy:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.lsock = []
        
        
    def run(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            s.listen(5)
            self.lsock.append(s)
            print('TCP Proxy listening on port', self.port)
            while True:
                rsock, wsock, esock = select.select(self.lsock, [], [])
                for sock in rsock:
                    print('Got a socket')
                    if sock == s:
                        self.accept_new_connection(s)
                    else:
                        self.data_from_client(sock)
        except KeyboardInterrupt:
            print('Exiting')
            s.close()
            sys.exit(0)
    
    def accept_new_connection(self, s):
        (csock, addr) = s.accept()
        self.lsock.append(csock)
        print('Got connection from', addr)
    
    def data_from_client(self, sock):
        data = sock.recv(1024)
        if not data:
            print('Closing connection to client')
            self.lsock.remove(sock)
            sock.close()
            return
        print('Client sent: ', data)
        sock.send(data)
        
        