# Entry point for the client

import sys
import os
from threading import Thread
from client import ConvertClient
from config import Config

from netfilterqueue import NetfilterQueue

def dummy_handle_packet(packet):
    print(packet)
    packet.accept()

def run_queue_thread(queue_num: int, interface: str, nfqueue):
    print(f'Running queue {queue_num} on interface {interface}')
    try:
        nfqueue.run()
    finally:
        os.system(f'iptables -D INPUT -i {interface} -j NFQUEUE --queue-num {queue_num}')
        os.system(f'iptables -D OUTPUT -o {interface} -j NFQUEUE --queue-num {queue_num}')
        

def enable_packet_queues(config: Config, client: ConvertClient):
    """
    Enable the queues for the client to intercept packets
    """
    queue_num = 0
    queues = []
    for interface in config.interfaces:
        # packets coming into the interface will be queued
        os.system(f'iptables -A INPUT -i {interface["name"]} -j NFQUEUE --queue-num {queue_num}')
        # packets going out of the interface will be queued
        os.system(f'iptables -A OUTPUT -o {interface["name"]} -j NFQUEUE --queue-num {queue_num}')
        
        # bind the queue to the client
        nfqueue = NetfilterQueue()
        nfqueue.bind(queue_num, client.on_packet)
        thread = Thread(target=run_queue_thread, args=(queue_num, interface["name"], nfqueue))
        thread.start()
        
        queues.append((nfqueue, thread, queue_num))
        
        queue_num += 1
        for _, thread, _ in queues:
            thread.join()
    return queues

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <config_file>')
        sys.exit(1)
    config_file = sys.argv[1]
    config = Config(config_file)
    
    client = ConvertClient(config.host, config.port)
    
    # set up the packet queue
    queues = enable_packet_queues(config, client)
    print(f'Enabled {len(queues)} packet queues')
    # keep the client running
    while True:
        pass