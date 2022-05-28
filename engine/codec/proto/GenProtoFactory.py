import re, io

proto_to_id = {}
method_to_id = {}

PY_PROTO_FACTORY_TEMPLATE = '''
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_name2type = dict()

{proto_id_code}
'''

CS_PROTO_FACTORY_TEMPLATE = '''
// do not edit. gen by server codec
using Google.Protobuf;

namespace WindNetwork
{
	public partial class ProtoFactoryPb
	{
		public static IMessage GetProtoObj(int protoId)
		{
			switch (protoId)
			{
{get_proto_obj_code}
			}
			return null;
		}

		public static IMessage DecodeProtoData(byte[] dataBytes, int protoId)
		{
			IMessage ret;
			switch (protoId)
			{
{decode_proto_data}
			}
			return null;
		}

		public static void Call(int protoId, IMessage m)
		{
			switch (protoId)
			{
{proto_callback_code}
			}
		}	

		public static int GetProtoId(string name)
		{
			switch (name)
			{
{get_id_code}
			}
			return 0;
		}
	}
}
'''


def load_menu(menu_path, menu_file, filters=None):
    proto_to_id.clear()
    method_to_id.clear()

    with open(f'{menu_path}/{menu_file}', 'r', encoding='UTF-8') as f:
        for pro_str in f.readlines():
            line = pro_str.split('=')
            if len(line) >= 2:
                str_key = line[0].strip()
                str_val = line[1].strip()
                if filters is not None and str_key not in filters:
                    continue
                proto_to_id[str_key] = int(str_val)

    for (proto, start_id) in proto_to_id.items():
        LoadMethod2Id(menu_path, proto, start_id)


def LoadMethod2Id(menu_path, proto_file, start_id):
    f = open('{}/{}'.format(menu_path, proto_file), 'r', encoding='utf-8')
    num_off = 1
    for now_str in f.readlines():
        m = re.match(r'^message[ \t]*(\w+).*$', now_str)
        if m is None:
            continue
        method_names = m.group(1)
        method_to_id[method_names] = start_id + num_off
        num_off = num_off + 1
    f.close()


def gen_proto_py(out_path):
    output_def = io.StringIO()
    output_mid = io.StringIO()
    output_name = io.StringIO()
    output_obj = io.StringIO()

    for (k, v) in method_to_id.items():
        output_def.write("proto_id2name[{}] = '{}'\n".format(v, k))
        output_mid.write("proto_name2id['{}'] = {}\n".format(k, v))
        output_name.write("str_{0} = '{0}'\n".format(k))
        output_obj.write("proto_name2type['{0}'] = {0}\n".format(k))

    final_str = output_def.getvalue()
    final_str += output_mid.getvalue()
    final_str += output_name.getvalue()
    final_str += output_obj.getvalue()
    fout = open(out_path, 'w', encoding='UTF-8', newline='')
    fout.write(
        PY_PROTO_FACTORY_TEMPLATE.format(proto_id_code=final_str))
    fout.close()


def gen_proto_cs(out_path):
    output_parse = io.StringIO()
    output_call = io.StringIO()

    output_mid = io.StringIO()
    output_ori = io.StringIO()

    for (k, v) in method_to_id.items():
        if k.endswith('Response'):

            output_parse.write("\t\t\t\tcase {}:\n".format(v))
            output_parse.write("\t\t\t\t\tret = {}.Parser.ParseFrom(dataBytes);\n".format(k))
            output_parse.write("\t\t\t\t\treturn ret;\n")

            output_call.write("\t\t\t\tcase {}:\n".format(v))
            output_call.write("\t\t\t\t\tWindHandler.On_{0}(({0})m);\n".format(k))
            output_call.write("\t\t\t\tbreak;\n")
            output_ori.write("\t\t\t\tcase {}:\n".format(v))
            output_ori.write("\t\t\t\t\tvar proto{} = new {}();\n".format(v, k))
            output_ori.write("\t\t\t\t\treturn proto{};\n".format(v))
        output_mid.write('\t\t\t\tcase \"{}\":\n'.format(k))
        output_mid.write("\t\t\t\t\treturn {};\n".format(v))

    fout = open(out_path, 'w', encoding='UTF-8', newline='')
    final_str = CS_PROTO_FACTORY_TEMPLATE.replace('{decode_proto_data}', output_parse.getvalue())
    final_str = final_str.replace('{get_proto_obj_code}', output_ori.getvalue())
    final_str = final_str.replace('{proto_callback_code}', output_call.getvalue())
    final_str = final_str.replace('{get_id_code}', output_mid.getvalue())
    fout.write(final_str)
    fout.close()


if __name__ == '__main__':
    # protoc 3.20 不在直接生成协议兑对象了 改成动态生成了
    # 这里使用
    load_menu('../engine/codec/proto/proto_client', 'menu.txt')
    gen_proto_py('../engine/codec/gen/proto_client/factory_client.py')

    gen_proto_cs('../sdks/unity/ProtoGen/GenProtoFactory.cs')
    print('success gen gen_proto_factory.proto_client')

    load_menu('../engine/codec/proto/proto_server', 'menu.txt')
    gen_proto_py('../engine/codec/gen/proto_server/factory_server.py')
    print('success gen factory_server.factory_server')

