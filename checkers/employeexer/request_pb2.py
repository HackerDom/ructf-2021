# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: request.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='request.proto',
  package='org',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rrequest.proto\x12\x03org\".\n\x08UserPair\x12\x10\n\x08username\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\"m\n\x10StrippedEmployee\x12\n\n\x02id\x18\x01 \x02(\t\x12\r\n\x05owner\x18\x02 \x02(\t\x12\x1b\n\x04name\x18\x03 \x02(\x0b\x32\r.org.FullName\x12\x13\n\x0b\x64\x65scription\x18\x04 \x02(\t\x12\x0c\n\x04tags\x18\x05 \x03(\t\"\x1d\n\nStringList\x12\x0f\n\x07strings\x18\x01 \x03(\t\"E\n\x11StrippedEmployees\x12\x30\n\x11strippedEmployees\x18\x01 \x03(\x0b\x32\x15.org.StrippedEmployee\"I\n\x08\x45mployee\x12\n\n\x02id\x18\x01 \x02(\t\x12\"\n\x08\x65mployee\x18\x02 \x02(\x0b\x32\x10.org.NewEmployee\x12\r\n\x05owner\x18\x03 \x02(\t\"\x8b\x01\n\x0bNewEmployee\x12\x1b\n\x04name\x18\x01 \x02(\x0b\x32\r.org.FullName\x12\x1b\n\x04\x63\x61rd\x18\x02 \x02(\x0b\x32\r.org.BankCard\x12\x1f\n\x08location\x18\x03 \x02(\x0b\x32\r.org.Location\x12\x13\n\x0b\x64\x65scription\x18\x04 \x02(\t\x12\x0c\n\x04tags\x18\x05 \x03(\t\"E\n\x08\x46ullName\x12\x11\n\tfirstName\x18\x01 \x02(\t\x12\x12\n\nsecondName\x18\x02 \x02(\t\x12\x12\n\nmiddleName\x18\x03 \x01(\t\";\n\x08\x42\x61nkCard\x12\x0e\n\x06number\x18\x01 \x02(\t\x12\x12\n\ncardholder\x18\x02 \x02(\t\x12\x0b\n\x03\x63vv\x18\x03 \x02(\t\")\n\x08Location\x12\x0f\n\x07\x63ountry\x18\x01 \x02(\t\x12\x0c\n\x04\x63ity\x18\x02 \x02(\t'
)




_USERPAIR = _descriptor.Descriptor(
  name='UserPair',
  full_name='org.UserPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='org.UserPair.username', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='org.UserPair.password', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=68,
)


_STRIPPEDEMPLOYEE = _descriptor.Descriptor(
  name='StrippedEmployee',
  full_name='org.StrippedEmployee',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='org.StrippedEmployee.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner', full_name='org.StrippedEmployee.owner', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='org.StrippedEmployee.name', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='org.StrippedEmployee.description', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='org.StrippedEmployee.tags', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=179,
)


_STRINGLIST = _descriptor.Descriptor(
  name='StringList',
  full_name='org.StringList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='strings', full_name='org.StringList.strings', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=181,
  serialized_end=210,
)


_STRIPPEDEMPLOYEES = _descriptor.Descriptor(
  name='StrippedEmployees',
  full_name='org.StrippedEmployees',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='strippedEmployees', full_name='org.StrippedEmployees.strippedEmployees', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=281,
)


_EMPLOYEE = _descriptor.Descriptor(
  name='Employee',
  full_name='org.Employee',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='org.Employee.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='employee', full_name='org.Employee.employee', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner', full_name='org.Employee.owner', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=283,
  serialized_end=356,
)


_NEWEMPLOYEE = _descriptor.Descriptor(
  name='NewEmployee',
  full_name='org.NewEmployee',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='org.NewEmployee.name', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='card', full_name='org.NewEmployee.card', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='location', full_name='org.NewEmployee.location', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='org.NewEmployee.description', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='org.NewEmployee.tags', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=498,
)


_FULLNAME = _descriptor.Descriptor(
  name='FullName',
  full_name='org.FullName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='firstName', full_name='org.FullName.firstName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secondName', full_name='org.FullName.secondName', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='middleName', full_name='org.FullName.middleName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=500,
  serialized_end=569,
)


_BANKCARD = _descriptor.Descriptor(
  name='BankCard',
  full_name='org.BankCard',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='org.BankCard.number', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cardholder', full_name='org.BankCard.cardholder', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cvv', full_name='org.BankCard.cvv', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=571,
  serialized_end=630,
)


_LOCATION = _descriptor.Descriptor(
  name='Location',
  full_name='org.Location',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='country', full_name='org.Location.country', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='city', full_name='org.Location.city', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=632,
  serialized_end=673,
)

_STRIPPEDEMPLOYEE.fields_by_name['name'].message_type = _FULLNAME
_STRIPPEDEMPLOYEES.fields_by_name['strippedEmployees'].message_type = _STRIPPEDEMPLOYEE
_EMPLOYEE.fields_by_name['employee'].message_type = _NEWEMPLOYEE
_NEWEMPLOYEE.fields_by_name['name'].message_type = _FULLNAME
_NEWEMPLOYEE.fields_by_name['card'].message_type = _BANKCARD
_NEWEMPLOYEE.fields_by_name['location'].message_type = _LOCATION
DESCRIPTOR.message_types_by_name['UserPair'] = _USERPAIR
DESCRIPTOR.message_types_by_name['StrippedEmployee'] = _STRIPPEDEMPLOYEE
DESCRIPTOR.message_types_by_name['StringList'] = _STRINGLIST
DESCRIPTOR.message_types_by_name['StrippedEmployees'] = _STRIPPEDEMPLOYEES
DESCRIPTOR.message_types_by_name['Employee'] = _EMPLOYEE
DESCRIPTOR.message_types_by_name['NewEmployee'] = _NEWEMPLOYEE
DESCRIPTOR.message_types_by_name['FullName'] = _FULLNAME
DESCRIPTOR.message_types_by_name['BankCard'] = _BANKCARD
DESCRIPTOR.message_types_by_name['Location'] = _LOCATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserPair = _reflection.GeneratedProtocolMessageType('UserPair', (_message.Message,), {
  'DESCRIPTOR' : _USERPAIR,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.UserPair)
  })
_sym_db.RegisterMessage(UserPair)

StrippedEmployee = _reflection.GeneratedProtocolMessageType('StrippedEmployee', (_message.Message,), {
  'DESCRIPTOR' : _STRIPPEDEMPLOYEE,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.StrippedEmployee)
  })
_sym_db.RegisterMessage(StrippedEmployee)

StringList = _reflection.GeneratedProtocolMessageType('StringList', (_message.Message,), {
  'DESCRIPTOR' : _STRINGLIST,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.StringList)
  })
_sym_db.RegisterMessage(StringList)

StrippedEmployees = _reflection.GeneratedProtocolMessageType('StrippedEmployees', (_message.Message,), {
  'DESCRIPTOR' : _STRIPPEDEMPLOYEES,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.StrippedEmployees)
  })
_sym_db.RegisterMessage(StrippedEmployees)

Employee = _reflection.GeneratedProtocolMessageType('Employee', (_message.Message,), {
  'DESCRIPTOR' : _EMPLOYEE,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.Employee)
  })
_sym_db.RegisterMessage(Employee)

NewEmployee = _reflection.GeneratedProtocolMessageType('NewEmployee', (_message.Message,), {
  'DESCRIPTOR' : _NEWEMPLOYEE,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.NewEmployee)
  })
_sym_db.RegisterMessage(NewEmployee)

FullName = _reflection.GeneratedProtocolMessageType('FullName', (_message.Message,), {
  'DESCRIPTOR' : _FULLNAME,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.FullName)
  })
_sym_db.RegisterMessage(FullName)

BankCard = _reflection.GeneratedProtocolMessageType('BankCard', (_message.Message,), {
  'DESCRIPTOR' : _BANKCARD,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.BankCard)
  })
_sym_db.RegisterMessage(BankCard)

Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), {
  'DESCRIPTOR' : _LOCATION,
  '__module__' : 'request_pb2'
  # @@protoc_insertion_point(class_scope:org.Location)
  })
_sym_db.RegisterMessage(Location)


# @@protoc_insertion_point(module_scope)
