# Entry point for the client

import sys
import os
import threading
from client import ConvertClient
from config import Config


from netfilterqueue import NetfilterQueue

def enable_packet_queues(config: Config, client: ConvertClient):
    """
    Enable the queues for the client to intercept packets
    """
    queue = 0
    threads = []
    
    def _start_queue(queue: int, iface: str, client: ConvertClient):
        nfqueue = NetfilterQueue()
        # packets coming into the interface will be queued
        os.system(f'iptables -A INPUT -i {iface} -j NFQUEUE --queue-num {queue}')
        # packets going out of the interface will be queued
        os.system(f'iptables -A OUTPUT -o {iface} -j NFQUEUE --queue-num {queue}')
        
        # bind the queue to the client
        nfqueue.bind(queue, client.on_packet)
        nfqueue.run()
        
    for interface in config.interfaces:
        t = threading.Thread(target=_start_queue, args=(queue, interface["name"], client))
        threads.append(t)
        queue += 1
    for t in threads:
        t.start()
        t.join()
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
        
        print('Client running...')
        for i in range(queues):
            print(f'\t[{i}] Queue running for interfaces {config.interfaces[i]["name"]}...')
        
        # keep the client running
        while True:
            pass
    finally:
        print('Shutting down...')
        # remove the iptables rules
        os.system(f'iptables -F')
        sys.exit(0)