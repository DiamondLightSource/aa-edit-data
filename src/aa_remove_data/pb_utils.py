import EPICSEvent_pb2


def unescape_data(data):
    # Reverse the escaping process
    data = data.replace(b'\x1B\x03', b'\x0D')  # Unescape carriage return
    data = data.replace(b'\x1B\x02', b'\x0A')  # Unescape newline
    data = data.replace(b'\x1B\x01', b'\x1B')  # Unescape escape character
    return data


def escape_data(data):
    # Replace escape character first to avoid conflicts
    data = data.replace(b'\x1B', b'\x1B\x01')
    data = data.replace(b'\x0A', b'\x1B\x02')  # Escape newline
    data = data.replace(b'\x0D', b'\x1B\x03')  # Escape carriage return
    return data


def convert_to_class_name(enum_name):
    # Split the enum name by underscores and capitalize each part
    parts = enum_name.split('_')
    return ''.join(part.capitalize() for part in parts)


def get_message_type(header):
    type_descriptor = header.DESCRIPTOR.fields_by_name["type"]
    enum_descriptor = type_descriptor.enum_type
    return enum_descriptor.values_by_number[header.type].name


def get_message_class(message_type):
    message_type_pascal = convert_to_class_name(message_type)
    message = getattr(EPICSEvent_pb2, message_type_pascal)
    return message


def read_pb(filepath):
    header = EPICSEvent_pb2.PayloadInfo()
    with open(filepath, 'rb') as f:
        first_line = unescape_data(f.readline().strip())
        header.ParseFromString(first_line)
        lines = f.readlines()
        message_type = get_message_type(header)
        message_class = get_message_class(message_type)
        messages = [message_class() for n in range(len(lines))]
        for i, message in enumerate(messages):
            line = unescape_data(lines[i].strip())
            message.ParseFromString(line)
    return header, messages


def write_pb(filepath, header, messages):
    header_bytes = escape_data(header.SerializeToString()) + b'\n'
    messages_bytes = [escape_data(message.SerializeToString()) + b'\n'
                      for message in messages]
    with open(filepath, "wb") as f:
        f.writelines([header_bytes] + messages_bytes)
