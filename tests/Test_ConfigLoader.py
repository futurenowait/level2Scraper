import os

import pytest
import configparser

from src.ConfigLoader import ConfigBase

FILE_PATH = os.path.abspath("../")

section_test_data = [
    ("bitmex","stream",
     {"url":"wss://www.bitmex.com/realtime",
      "symbols":["XBTUSD","ETHUSD"],
      "retry_connections": 10
      }),
    ("bitmex","process",
     {"batch_size":1000,
      "use_compression":False,
      "aggregation_interval":24}),
    (None,"zeromq",
     {"port":"5556"})
]


def test_pkg_resource_path():



    regular_config = ConfigBase(config_type="not_relevant",exchange=None,test_mode=False)
    test_config = ConfigBase(config_type="not_relevant",exchange=None,test_mode=True)

    assert  regular_config._resource_path == FILE_PATH+"/src/config.ini", "Wrong regular config file path"
    assert  test_config._resource_path == FILE_PATH+"/tests/test_config.ini", "Wrong test config file path"


def test_config_file_syntax():
    config = configparser.ConfigParser()
    config.read(FILE_PATH+"/tests/test_config.ini")


    for section in config.keys():
        if section == "DEFAULT":
            assert list(config['DEFAULT'].keys()) == []
        else:
            if "STREAM" in section:
                section_split = section.split('.')
                assert section_split[0] == "STREAM"

            elif "DP" in section:
                pass

            elif "ZEROMQ" in section:
                pass


@pytest.mark.parametrize("exchange,section,expected",section_test_data)
def test_section_handling(exchange,section,expected):

    test_config = ConfigBase(config_type="not_relevant",exchange=None,test_mode=True)

    test_config._load_config(section,exchange)

    for key in expected:
        assert getattr(test_config,"_"+key) == expected[key]
