import EPICSEvent_pb2
from google.protobuf.message import Message
from typing import Optional, Type
from os import PathLike


class PBUtils:

    def __init__(self, filepath: Optional[PathLike] = None):
        self.header = EPICSEvent_pb2.PayloadInfo()
        self.messages = []
        self.message_type = ''
        if filepath:
            self.read_pb(filepath)

    def _unescape_data(self, data: bytes) -> bytes:
        # Reverse the escaping process
        data = data.replace(b'\x1B\x03', b'\x0D')  # Unescape carriage return
        data = data.replace(b'\x1B\x02', b'\x0A')  # Unescape newline
        data = data.replace(b'\x1B\x01', b'\x1B')  # Unescape escape character
        return data

    def _escape_data(self, data: bytes) -> bytes:
        # Replace escape character first to avoid conflicts
        data = data.replace(b'\x1B', b'\x1B\x01')
        data = data.replace(b'\x0A', b'\x1B\x02')  # Escape newline
        data = data.replace(b'\x0D', b'\x1B\x03')  # Escape carriage return
        return data

    def _convert_to_class_name(self, enum_name: str) -> str:
        # Split the enum name by underscores and capitalize each part
        parts = enum_name.split('_')
        return ''.join(part.capitalize() for part in parts)

    def get_message_type(self) -> str:
        type_descriptor = self.header.DESCRIPTOR.fields_by_name["type"]
        enum_descriptor = type_descriptor.enum_type
        return enum_descriptor.values_by_number[self.header.type].name

    def get_message_class(self) -> Type[Message]:
        # Ensure self.message_type is set first.
        if not self.message_type:
            self.message_type = self.get_message_type()
        message_type_camel = self._convert_to_class_name(self.message_type)
        message_class = getattr(EPICSEvent_pb2, message_type_camel)
        return message_class

    def read_pb(self, filepath: PathLike):
        with open(filepath, 'rb') as f:
            first_line = self._unescape_data(f.readline().strip())
            self.header.ParseFromString(first_line)
            message_class = self.get_message_class()
            lines = f.readlines()
            self.messages = [message_class() for n in range(len(lines))]
            for i, message in enumerate(self.messages):
                line = self._unescape_data(lines[i].strip())
                message.ParseFromString(line)

    def write_pb(self, filepath: PathLike):
        header_b = self._escape_data(self.header.SerializeToString()) + b'\n'
        messages_b = [self._escape_data(message.SerializeToString()) + b'\n'
                      for message in self.messages]
        with open(filepath, "wb") as f:
            f.writelines([header_b] + messages_b)
