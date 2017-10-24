
from collections import namedtuple
from enum import Enum, unique, auto
from html.parser import HTMLParser


GenType = namedtuple('GenType', ['typename', 'comment', 'properties'])
PropertyType = namedtuple('PropertyType', ['name', 'typename', 'comment'])


@unique
class WriteMode(Enum):
    NONE = auto()
    TYPENAME = auto()
    WAIT_FOR_FIRST_PROPS = auto()
    FIND_PROPERTY_NAME = auto()
    WAIT_FOR_NEXT_PROP = auto()
    WRITE_PROPERTY_NAME = auto()
    FIND_PROPERTY_TYPE = auto()
    WRITE_PROPERTY_TYPE = auto()
    FIND_PROPERTY_COMMENT = auto()
    WRITE_PROPERTY_COMMENT = auto()
    COMMIT = auto()
    COMMIT_PROPERTY = auto()
    COMMENT = auto()


class ApiRefPageParser(HTMLParser):
    def __init__(self):
        super(ApiRefPageParser, self).__init__()
        self._types = []

        self._reset_current()

    @property
    def types(self):
        return self._types

    def handle_starttag(self, tag, attrs):
        if tag == 'h5':
            self._write_mode = WriteMode.TYPENAME

        elif tag == 'tbody' and self._write_mode == WriteMode.WAIT_FOR_FIRST_PROPS:
            self._write_mode = WriteMode.FIND_PROPERTY_NAME

        elif tag == 'tr' and self._write_mode == WriteMode.WAIT_FOR_NEXT_PROP:
            self._write_mode = WriteMode.FIND_PROPERTY_NAME

        elif tag == 'td':
            if self._write_mode == WriteMode.FIND_PROPERTY_NAME:
                self._write_mode = WriteMode.WRITE_PROPERTY_NAME

            elif self._write_mode == WriteMode.FIND_PROPERTY_TYPE:
                self._write_mode = WriteMode.WRITE_PROPERTY_TYPE

            elif self._write_mode == WriteMode.FIND_PROPERTY_COMMENT:
                self._write_mode = WriteMode.WRITE_PROPERTY_COMMENT

    def handle_endtag(self, tag):
        if tag == 'div' and self._write_mode == WriteMode.COMMIT:
            self._write_current()

        elif tag == 'tr' and self._write_mode == WriteMode.COMMIT_PROPERTY:
            self._write_current_property()
            self._write_mode = WriteMode.WAIT_FOR_NEXT_PROP

        elif tag == 'tbody' and self._write_mode == WriteMode.WAIT_FOR_NEXT_PROP:
            self._write_mode = WriteMode.COMMIT
        

    def handle_data(self, data):
        if self._write_mode == WriteMode.TYPENAME:
            self._current_typename = data.strip()
            self._write_mode = WriteMode.COMMENT

        elif self._write_mode == WriteMode.COMMENT:
            self._current_comment = data.strip(" \r\n\t-")
            self._write_mode = WriteMode.WAIT_FOR_FIRST_PROPS

        elif self._write_mode == WriteMode.WRITE_PROPERTY_NAME:
            self._current_property_name = data.strip()
            self._write_mode = WriteMode.FIND_PROPERTY_TYPE

        elif self._write_mode == WriteMode.WRITE_PROPERTY_TYPE:
            self._current_property_typename = data.strip()
            self._write_mode = WriteMode.FIND_PROPERTY_COMMENT

        elif self._write_mode == WriteMode.WRITE_PROPERTY_COMMENT:
            self._current_property_comment = data.strip(" \r\n\t-")
            self._write_mode = WriteMode.COMMIT_PROPERTY
    
    @property
    def _write_mode(self):
        return self.__write_mode

    @_write_mode.setter
    def _write_mode(self, val):
        self.__write_mode = val

    def _reset_current_property(self):
        self._current_property_name = None
        self._current_property_comment = None
        self._current_property_typename = None

    def _reset_current(self):
        self._current_typename = None
        self._current_comment = None
        self._current_properties = []

        self._reset_current_property()

        self._write_mode = WriteMode.NONE
    
    def _write_current(self):
        self._types.append(GenType(self._current_typename, self._current_comment, frozenset(self._current_properties)))
        self._reset_current()

    def _write_current_property(self):
        self._current_properties.append(
            PropertyType(
                self._current_property_name,
                self._current_property_typename,
                self._current_property_comment
            )
        )

        self._reset_current_property()
