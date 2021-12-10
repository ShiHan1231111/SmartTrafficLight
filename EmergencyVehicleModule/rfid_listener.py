from read_mifare import *
import asyncio
from Firebase import Firebase

FB = Firebase()


class rfid_listener(object):
    def __init__(self):
        self._id, self._text = reader.read()

    @property
    def id_and_text(self):
        return self._id, self._text

    @id_and_text.setter
    def id_and_text(self, val):
        if (self._id, self._text) != val:
            (self._id, self._text) = val
