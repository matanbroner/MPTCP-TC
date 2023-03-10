import yaml

class Config:
    interfaces = None
    host = None
    port = None
    transport_converter = { "host": None, "port": None }
    
    def __init__(self, yaml_file: str):
        self.parse(yaml_file)
        
    def parse(self, filename: str):
        with open(filename, "r") as f:
            config = yaml.safe_load(f)
            config = config["client"]
            self.interfaces = config["interfaces"]
            self.transport_converter["host"] = config["transport_converter"]["host"]
            self.transport_converter["port"] = config["transport_converter"]["port"]
    