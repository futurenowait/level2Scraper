import configparser
import pkg_resources

class ConfigBase(object):
    def __init__(self,config_type,exchange=None):
        self._load_config(config_type,exchange)

    def _streamer_section(self,section_name):
        config = configparser.ConfigParser()
        resource_path = pkg_resources.resource_filename("src","config.ini")
        config.read(resource_path)

        self._url = config.get(section_name,'url',
                                fallback="{0} Section does not have {1} variable\n".format(section_name,"url"))

        symbols_to_test = config.get(section_name,"symbols",
                                     fallback=None)
        if symbols_to_test:

            if Helpers.ensure_correct_symbols_bitmex(symbols_to_test.split(',')):
                self._symbols = symbols_to_test.split(',')

            else:
                print("Not Supported Symbols Found\nCould be Formatting\nExiting...")

        self._retry_connections = config.get(section_name,'max_retry_connections',
                                              fallback="{0} Section does not have {1} variable\n"
                                              .format(section_name,"max_retry_connections"))

    def _processor_section(self,section_name):
        config = configparser.ConfigParser()
        resource_path = pkg_resources.resource_filename("src", "config.ini")
        config.read(resource_path)

        self._batch_size = config.get(section_name,'batch_size',
                                       fallback="")
        self._use_compression = \
            True if config['DATA_PROCESS']['use_compression'].upper() == "TRUE" else False
        self._aggregation_interval = config['DATA_PROCESS']['data_aggregation_interval']

    def _zeromq_section(self):
        config = configparser.ConfigParser()
        resource_path = pkg_resources.resource_filename("src", "config.ini")
        config.read(resource_path)

        self._port = config.get("ZEROMQ","port",
                                fallback="No valid port for ZeroMQ")

    def _load_config(self,c_type,exchange):

        try:
            if c_type.upper() == "STREAM":
                if exchange:
                    self._streamer_section("STREAM."+exchange.upper())

            elif c_type.upper() == "PROCESS":
                if exchange:
                    self._processor_section("DP."+exchange.upper())
            elif c_type.upper() == "ZEROMQ":
                self._zeromq_section()

        except Exception as error:
            print("{0}: {1}".format(type(error).__name__,error))





class Helpers:

    @classmethod
    def ensure_correct_symbols_bitmex(cls,symbols_list):
        supported_symbols = ["XBTUSD", "ETHUSD", "XRPUSD", "ADAU20", "BCHUSD", "EOSU20", "LTCU20", "TRXU20"]

        return all(symbol in supported_symbols for symbol in symbols_list)


