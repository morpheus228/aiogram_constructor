class UnsatisfactoryEnviroment(Exception):
    def __init__(self, block_type: type, missing_attribute: str):
        self.block_type: type = block_type
        self.missing_attribute: str = missing_attribute

    def __str__(self):
        return f"'{self.missing_attribute}' attribute omitted during initialization '{self.block_type}'"