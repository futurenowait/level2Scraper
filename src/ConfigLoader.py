import configparser
import pkg_resources

class ConfigBase:
    def __init__(self,config_type):
        self.__load_config(config_type)

    def __streamer_section(self):
        config = configparser.ConfigParser()
        resource_path = pkg_resources.resource_filename("src","config.ini")
        config.read(resource_path)

        self.__url = config['STREAM']['url']

        if Helpers.ensure_correct_symbols(config['STREAM']['symbols'].split(',')):
            self.__symbols = config['STREAM']['symbols'].split(',')
        else:
            print("Not Supported Symbols Found\nCould be Formatting\nExiting...")

        self.__retry_connections = config['STREAM']['max_retry_connections']

    def __processor_section(self):
        config = configparser.ConfigParser()
        resource_path = pkg_resources.resource_filename("src", "config.ini")
        config.read(resource_path)

        self.__batch_size = config['DATA_PROCESS']['batch_size']
        self.__use_compression = \
            True if config['DATA_PROCESS']['use_compression'].upper() == "TRUE" else False
        self.__aggregation_interval = config['DATA_PROCESS']['data_aggregation_interval']

    def __load_config(self,c_type):

        try:
            if c_type.upper() == "STREAM":
                self.__streamer_section()
            elif c_type.upper() == "PROCESS":
                self.__processor_section()

        except Exception as error:
            print("{0}: {1}".format(type(error).__name__,error))





class Helpers:

    @classmethod
    def ensure_correct_symbols(cls,symbols_list):
        supported_symbols = ["XBTUSD", "ETHUSD", "XRPUSD", "ADAU20", "BCHUSD", "EOSU20", "LTCU20", "TRXU20"]

        return all(symbol in supported_symbols for symbol in symbols_list)


