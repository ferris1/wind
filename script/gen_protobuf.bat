

protoc-3.19.2.exe --proto_path=../engine/codec/proto/rpc_server --proto_path=../engine/codec/proto/google  --python_out=../engine/codec/gen/rpc_server  ../engine/codec/proto/rpc_server/*.proto
protoc-3.19.2.exe --proto_path=../engine/codec/proto/rpc_client --proto_path=../engine/codec/proto/google  --python_out=../engine/codec/gen/rpc_client  ../engine/codec/proto/rpc_client/*.proto
protoc-3.19.2.exe --proto_path=../engine/codec/proto/rpc_client --proto_path=../engine/codec/proto/google  --csharp_out=../sdks/unity/ ../engine/codec/proto/rpc_client/*.proto


python ../engine/codec/proto/GenProtoFactory.py
pause