import EPICSEvent_pb2


class PBUtils:

    def __init__(self, filepath=None):
        self.header = EPICSEvent_pb2.PayloadInfo()
        self.messages = []
        self.message_type = ''
        if filepath:
            self.read_pb(filepath)

    def _unescape_data(self, data):
        # Reverse the escaping process
        data = data.replace(b'\x1B\x03', b'\x0D')  # Unescape carriage return
        data = data.replace(b'\x1B\x02', b'\x0A')  # Unescape newline
        data = data.replace(b'\x1B\x01', b'\x1B')  # Unescape escape character
        return data

    def _escape_data(self, data):
        # Replace escape character first to avoid conflicts
        data = data.replace(b'\x1B', b'\x1B\x01')
        data = data.replace(b'\x0A', b'\x1B\x02')  # Escape newline
        data = data.replace(b'\x0D', b'\x1B\x03')  # Escape carriage return
        return data

    def _convert_to_class_name(self, enum_name):
        # Split the enum name by underscores and capitalize each part
        parts = enum_name.split('_')
        return ''.join(part.capitalize() for part in parts)

    def _get_message_type(self, header):
        type_descriptor = header.DESCRIPTOR.fields_by_name["type"]
        enum_descriptor = type_descriptor.enum_type
        return enum_descriptor.values_by_number[header.type].name

    def get_message_class(self):
        message_type_camel = self._convert_to_class_name(self.message_type)
        message_class = getattr(EPICSEvent_pb2, message_type_camel)
        return message_class

    def read_pb(self, filepath):
        with open(filepath, 'rb') as f:
            first_line = self._unescape_data(f.readline().strip())
            self.header.ParseFromString(first_line)
            self.message_type = self._get_message_type(self.header)
            message_class = self.get_message_class()
            lines = f.readlines()
            self.messages = [message_class() for n in range(len(lines))]
            for i, message in enumerate(self.messages):
                line = self._unescape_data(lines[i].strip())
                message.ParseFromString(line)

    def write_pb(self, filepath):
        header_b = self._escape_data(self.header.SerializeToString()) + b'\n'
        messages_b = [self._escape_data(message.SerializeToString()) + b'\n'
                      for message in self.messages]
        with open(filepath, "wb") as f:
            f.writelines([header_b] + messages_b)
