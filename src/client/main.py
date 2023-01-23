# Entry point for the client

import sys
import os
from threading import Thread
from client import ConvertClient
from config import Config

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <config_file>')
        sys.exit(1)
        
    # load the config file
    config_file = sys.argv[1]
    config = Config(config_file)

    # create the client
    client = ConvertClient(config.host, config.port)
    
    # keep the server running
    while True:
        pass