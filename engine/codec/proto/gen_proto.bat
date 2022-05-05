


protoc-3.19.2.exe --proto_path=rpc_client --proto_path=google  --python_out=../gen/rpc_client  ./rpc_client/*.proto
protoc-3.19.2.exe --proto_path=rpc_client --proto_path=google  --csharp_out=../gen/cs ./rpc_client/*.proto


python GenProtoFactory.py
pause