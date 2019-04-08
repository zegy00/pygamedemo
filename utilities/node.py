class Node:
    def __init__(self, dataval):
        self._dataval = dataval
        self._nextval = None

    def set_next(self, nextval):
        self._nextval = nextval

    def next(self):
        return self._nextval

    def get_value(self):
        return self._dataval
