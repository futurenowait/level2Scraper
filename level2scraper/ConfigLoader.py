import configparser
import pkg_resources

class ConfigBase(object):
    def __init__(self,config_type,exchange=None,test_mode=False):
        """
        :type config_type:string
        :param config_type: Used for building configuration. Available types [Stream, Process, ZeroMQ]

        :type exchange:string
        :param exchange: Trading Exchange Name, it will automatically link with configuration section in config.ini file

        :type test_mode:boolean
        :param test_mode: Used to change object state which allows to test this object more conveniently
        """
        if test_mode:
            self._resource_path = pkg_resources.resource_filename("tests", "test_config.ini")
        else:
            self._resource_path = pkg_resources.resource_filename("level2scraper","config.ini")
            self._load_config(config_type,exchange)

    def _streamer_section(self,section_name):
        """
        Reads Streamer type configuration and initializes variables [url,symbols,retry_connection] for future uses
        :type section_name: string
        :param section_name: Used for accessing correct section in config.ini file
        :return:
        """
        config = configparser.ConfigParser()
        config.read(self._resource_path)


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

        try:
            self._retry_connections = int(self._retry_connections)
        except Exception as error:
            print(error)

    def _processor_section(self,section_name):
        """
        Reads Data Processor type configuration and initializes variables:
            batch_size: int,
            use_compression: bool,
            aggregation_interval: int


        :type section_name: string
        :param section_name: Used for accessing correct section in config.ini file
        :return:
        """
        config = configparser.ConfigParser()
        config.read(self._resource_path)

        self._batch_size = config.get(section_name,'batch_size',
                                       fallback="")

        try:
            self._batch_size = int(self._batch_size)
        except Exception as error:
            print(error)

        self._use_compression = \
            True if config.get(section_name,"use_compression",fallback="false").upper() == "TRUE" else False
        self._aggregation_interval = config.get(section_name,"data_aggregation_interval",
                                                fallback=24)

        try:
            self._aggregation_interval = int(self._aggregation_interval)
        except Exception as error:
            print(error)

    def _zeromq_section(self):
        """
        Reads ZeroMQ type configuration and initializes variables:
            port: string
        :return:
        """
        config = configparser.ConfigParser()
        config.read(self._resource_path)

        self._port = config.get("ZEROMQ","port",
                                fallback="No valid port for ZeroMQ")

    def _load_config(self,c_type,exchange):
        """
        Routing configuration loading

        :type c_type: string
        :param c_type: Used for routing

        :type exchange: string
        :param exchange: Used for building section_name that is passed to specific configuration handlers
        :return:
        """
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
        """
        Helper function that checks if symbols that will be used to subscribe to websocket are legit

        :type symbols_list: list(string)
        :param symbols_list:
        :return:
        """
        supported_symbols = ["XBTUSD", "ETHUSD", "XRPUSD", "ADAU20", "BCHUSD", "EOSU20", "LTCU20", "TRXU20"]

        return all(symbol in supported_symbols for symbol in symbols_list)


