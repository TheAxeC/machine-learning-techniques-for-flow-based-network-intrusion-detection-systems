

# The config class
class Config:

    def __init__(self):
        self.default = 'config.cnf'

    # Reading the config file
    def read_config(self, file=None):
        import ConfigParser

        try:
            config = ConfigParser.ConfigParser()
            if file:
                config.read(file)
            else:
                config.read(self.default)



        except Exception as e:
            pass
