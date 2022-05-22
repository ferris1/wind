

protoc-3.19.2.exe --proto_path=../engine/codec/proto/proto_server --proto_path=../engine/codec/proto/google  --python_out=../engine/codec/gen/proto_server  ../engine/codec/proto/proto_server/*.proto
protoc-3.19.2.exe --proto_path=../engine/codec/proto/proto_client --proto_path=../engine/codec/proto/google  --python_out=../engine/codec/gen/proto_client  ../engine/codec/proto/proto_client/*.proto
protoc-3.19.2.exe --proto_path=../engine/codec/proto/proto_client --proto_path=../engine/codec/proto/google  --csharp_out=../sdks/unity/ProtoGen/ ../engine/codec/proto/proto_client/*.proto


python ../engine/codec/proto/GenProtoFactory.py
pause