# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Player.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cPlayer.proto\"\'\n\x12PlayerLoginRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\"8\n\x13PlayerLoginResponse\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\x08\"7\n\x11\x43reateRoleRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x0f\n\x07role_id\x18\x02 \x01(\x05\"H\n\x12\x43reateRoleResponse\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x0f\n\x07role_id\x18\x02 \x01(\x05\x12\x0e\n\x06result\x18\x03 \x01(\x08\"G\n\x13SpeakOnWorldRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"G\n\x14SpeakOnWorldResponse\x12\x10\n\x08speak_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\tb\x06proto3')



_PLAYERLOGINREQUEST = DESCRIPTOR.message_types_by_name['PlayerLoginRequest']
_PLAYERLOGINRESPONSE = DESCRIPTOR.message_types_by_name['PlayerLoginResponse']
_CREATEROLEREQUEST = DESCRIPTOR.message_types_by_name['CreateRoleRequest']
_CREATEROLERESPONSE = DESCRIPTOR.message_types_by_name['CreateRoleResponse']
_SPEAKONWORLDREQUEST = DESCRIPTOR.message_types_by_name['SpeakOnWorldRequest']
_SPEAKONWORLDRESPONSE = DESCRIPTOR.message_types_by_name['SpeakOnWorldResponse']
PlayerLoginRequest = _reflection.GeneratedProtocolMessageType('PlayerLoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERLOGINREQUEST,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:PlayerLoginRequest)
  })
_sym_db.RegisterMessage(PlayerLoginRequest)

PlayerLoginResponse = _reflection.GeneratedProtocolMessageType('PlayerLoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERLOGINRESPONSE,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:PlayerLoginResponse)
  })
_sym_db.RegisterMessage(PlayerLoginResponse)

CreateRoleRequest = _reflection.GeneratedProtocolMessageType('CreateRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEROLEREQUEST,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:CreateRoleRequest)
  })
_sym_db.RegisterMessage(CreateRoleRequest)

CreateRoleResponse = _reflection.GeneratedProtocolMessageType('CreateRoleResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEROLERESPONSE,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:CreateRoleResponse)
  })
_sym_db.RegisterMessage(CreateRoleResponse)

SpeakOnWorldRequest = _reflection.GeneratedProtocolMessageType('SpeakOnWorldRequest', (_message.Message,), {
  'DESCRIPTOR' : _SPEAKONWORLDREQUEST,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:SpeakOnWorldRequest)
  })
_sym_db.RegisterMessage(SpeakOnWorldRequest)

SpeakOnWorldResponse = _reflection.GeneratedProtocolMessageType('SpeakOnWorldResponse', (_message.Message,), {
  'DESCRIPTOR' : _SPEAKONWORLDRESPONSE,
  '__module__' : 'Player_pb2'
  # @@protoc_insertion_point(class_scope:SpeakOnWorldResponse)
  })
_sym_db.RegisterMessage(SpeakOnWorldResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PLAYERLOGINREQUEST._serialized_start=16
  _PLAYERLOGINREQUEST._serialized_end=55
  _PLAYERLOGINRESPONSE._serialized_start=57
  _PLAYERLOGINRESPONSE._serialized_end=113
  _CREATEROLEREQUEST._serialized_start=115
  _CREATEROLEREQUEST._serialized_end=170
  _CREATEROLERESPONSE._serialized_start=172
  _CREATEROLERESPONSE._serialized_end=244
  _SPEAKONWORLDREQUEST._serialized_start=246
  _SPEAKONWORLDREQUEST._serialized_end=317
  _SPEAKONWORLDRESPONSE._serialized_start=319
  _SPEAKONWORLDRESPONSE._serialized_end=390
# @@protoc_insertion_point(module_scope)
