# Entry point for the client

import sys
import os
from client import ConvertClient
from config import Config

from netfilterqueue import NetfilterQueue

def enable_packet_queues(config: Config, client: ConvertClient):
    """
    Enable the queues for the client to intercept packets
    """
    queue = 0
    nfqueue = NetfilterQueue()
    for interface in config.interfaces:
        # packets coming into the interface will be queued
        os.system(f'iptables -A INPUT -i {interface["name"]} -j NFQUEUE --queue-num {queue}')
        # packets going out of the interface will be queued
        os.system(f'iptables -A OUTPUT -o {interface["name"]} -j NFQUEUE --queue-num {queue}')
        
        # bind the queue to the client
        nfqueue.bind(queue, client.on_packet)
        nfqueue.run(block=False)
        
        queue += 1
    return queue

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print('Usage: python main.py <config_file>')
            sys.exit(1)
        config_file = sys.argv[1]
        config = Config(config_file)
        
        client = ConvertClient(config.host, config.port)
        
        # set up the packet queue
        queues = enable_packet_queues(config, client)
        
        # keep the client running
        while True:
            pass
    except KeyboardInterrupt:
        print('Shutting down...')
        # remove the iptables rules
        for i in range(queues):
            os.system(f'iptables -D INPUT -j NFQUEUE --queue-num {i}')
            os.system(f'iptables -D OUTPUT -j NFQUEUE --queue-num {i}')
        sys.exit(0)