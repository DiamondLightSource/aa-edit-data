from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
SCALAR_BYTE: PayloadType
SCALAR_DOUBLE: PayloadType
SCALAR_ENUM: PayloadType
SCALAR_FLOAT: PayloadType
SCALAR_INT: PayloadType
SCALAR_SHORT: PayloadType
SCALAR_STRING: PayloadType
V4_GENERIC_BYTES: PayloadType
WAVEFORM_BYTE: PayloadType
WAVEFORM_DOUBLE: PayloadType
WAVEFORM_ENUM: PayloadType
WAVEFORM_FLOAT: PayloadType
WAVEFORM_INT: PayloadType
WAVEFORM_SHORT: PayloadType
WAVEFORM_STRING: PayloadType

class FieldValue(_message.Message):
    __slots__ = ["name", "val"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    val: str
    def __init__(self, name: _Optional[str] = ..., val: _Optional[str] = ...) -> None: ...

class PayloadInfo(_message.Message):
    __slots__ = ["elementCount", "headers", "pvname", "type", "unused00", "unused01", "unused02", "unused03", "unused04", "unused05", "unused06", "unused07", "unused08", "unused09", "year"]
    ELEMENTCOUNT_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    PVNAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNUSED00_FIELD_NUMBER: _ClassVar[int]
    UNUSED01_FIELD_NUMBER: _ClassVar[int]
    UNUSED02_FIELD_NUMBER: _ClassVar[int]
    UNUSED03_FIELD_NUMBER: _ClassVar[int]
    UNUSED04_FIELD_NUMBER: _ClassVar[int]
    UNUSED05_FIELD_NUMBER: _ClassVar[int]
    UNUSED06_FIELD_NUMBER: _ClassVar[int]
    UNUSED07_FIELD_NUMBER: _ClassVar[int]
    UNUSED08_FIELD_NUMBER: _ClassVar[int]
    UNUSED09_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    elementCount: int
    headers: _containers.RepeatedCompositeFieldContainer[FieldValue]
    pvname: str
    type: PayloadType
    unused00: float
    unused01: float
    unused02: float
    unused03: float
    unused04: float
    unused05: float
    unused06: float
    unused07: float
    unused08: float
    unused09: str
    year: int
    def __init__(self, type: _Optional[_Union[PayloadType, str]] = ..., pvname: _Optional[str] = ..., year: _Optional[int] = ..., elementCount: _Optional[int] = ..., unused00: _Optional[float] = ..., unused01: _Optional[float] = ..., unused02: _Optional[float] = ..., unused03: _Optional[float] = ..., unused04: _Optional[float] = ..., unused05: _Optional[float] = ..., unused06: _Optional[float] = ..., unused07: _Optional[float] = ..., unused08: _Optional[float] = ..., unused09: _Optional[str] = ..., headers: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ...) -> None: ...

class ScalarByte(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: bytes
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[bytes] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarDouble(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: float
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[float] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarEnum(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: int
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[int] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarFloat(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: float
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[float] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarInt(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: int
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[int] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarShort(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: int
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[int] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class ScalarString(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: str
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[str] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class V4GenericBytes(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "userTag", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USERTAG_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    userTag: int
    val: bytes
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[bytes] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ..., userTag: _Optional[int] = ...) -> None: ...

class VectorChar(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: bytes
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[bytes] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorDouble(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[float]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorEnum(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[int]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorFloat(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[float]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorInt(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[int]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorShort(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[int]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class VectorString(_message.Message):
    __slots__ = ["fieldactualchange", "fieldvalues", "nano", "repeatcount", "secondsintoyear", "severity", "status", "val"]
    FIELDACTUALCHANGE_FIELD_NUMBER: _ClassVar[int]
    FIELDVALUES_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    REPEATCOUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDSINTOYEAR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    fieldactualchange: bool
    fieldvalues: _containers.RepeatedCompositeFieldContainer[FieldValue]
    nano: int
    repeatcount: int
    secondsintoyear: int
    severity: int
    status: int
    val: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, secondsintoyear: _Optional[int] = ..., nano: _Optional[int] = ..., val: _Optional[_Iterable[str]] = ..., severity: _Optional[int] = ..., status: _Optional[int] = ..., repeatcount: _Optional[int] = ..., fieldvalues: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ..., fieldactualchange: bool = ...) -> None: ...

class PayloadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
