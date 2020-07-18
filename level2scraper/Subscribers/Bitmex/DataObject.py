
class BitmexDataIterator():
    def __init__(self,data):
        self._data = data
        self._index = 0

    def __next__(self):
        pass

class BitmexDataStructure():
    """
    Data Object for Bitmex data manipulation
    """

    def __init__(self,symbol,use_compression=False):
        self._symbol = symbol
        self._header = None
        self._data = None
        self._size = None
        self._use_compression = use_compression

    def add_data(self,data):
        if self._data:
            self._ensure_correct_data_format(data)
            pass
        else:
            pass

    def save_data(self):
        if self._use_compression:
            pass
        else:
            pass
    def _ensure_correct_data_format(self,data_to_compare):
        pass

    def __iter__(self):
        return BitmexDataIterator(self)