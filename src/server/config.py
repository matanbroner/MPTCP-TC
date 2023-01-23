import yaml

class Config:
    interfaces = None
    host = None
    port = None
    
    def __init__(self, yaml_file: str):
        self.parse(yaml_file)
        
    def parse(self, filename: str):
        with open(filename, "r") as f:
            config = yaml.safe_load(f)
            config = config["server"]
            self.host = config["host"]
            self.port = config["port"]
    