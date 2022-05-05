import re, io

proto_to_id = {}
method_to_id = {}

PY_PROTO_FACTORY_TEMPLATE = '''
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_id2type = dict()

{class_id_statement}
'''

CS_PROTO_FACTORY_TEMPLATE = '''
using System;
using System.Collections.Generic;
using Google.Protobuf;

namespace NetworkCodec
{
	public partial class {class_name}
	{
		public static IMessage GetProtoObj(int proto_id)
		{
			switch (proto_id)
			{
{ori_class_statement}
			}
			return null;
		}

		public static IMessage GetProtoObj(byte[] _buf, ref int idx, out int proto_id)
		{
			proto_id = Misc.short_from_bytes_le(_buf, ref idx);
			int data_size = Misc.int_from_bytes_le(_buf, ref idx);
			var data_sequence = new byte[data_size];
			Array.Copy(_buf, idx, data_sequence, 0, data_sequence.Length);
			idx += data_size;
			IMessage ret;
			switch (proto_id)
			{
{class_id_statement}
			}
			return null;
		}

		public static void Call(int protoId, IMessage m)
		{
			switch (protoId)
			{
{class_call_statement}
			}
		}	

		public static int GetProtoId(string name)
		{
			switch (name)
			{
{class_mid_statement}
			}
			return 0;
		}	
{class_def}
	}
}
'''


def load_meta(menu_path, menu_file, filters=None):
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
        output_obj.write("proto_id2type['{0}'] = {0}\n".format(k))

    final_str = output_def.getvalue()
    final_str += output_mid.getvalue()
    final_str += output_name.getvalue()
    final_str += output_obj.getvalue()
    fout = open(out_path, 'w', encoding='UTF-8', newline='')
    fout.write(
        PY_PROTO_FACTORY_TEMPLATE.format(class_id_statement=final_str))
    fout.close()


def gen_proto_cs(out_path, class_name):
    output_parse = io.StringIO()
    output_call = io.StringIO()
    output_def = io.StringIO()
    output_mid = io.StringIO()
    output_ori = io.StringIO()

    for (k, v) in method_to_id.items():

        if k.endswith('Response'):
            output_parse.write("\t\t\t\tcase {}:\n".format(v))
            output_parse.write("\t\t\t\t\tret = {}.Parser.ParseFrom(data_sequence);\n".format(k))
            output_parse.write("\t\t\t\t\treturn ret;\n")

            output_call.write("\t\t\t\tcase {}:\n".format(v))
            output_call.write("\t\t\t\t\tServerRpcImplement.On_{0}(({0})m);\n".format(k))
            output_call.write("\t\t\t\tbreak;\n")
            output_ori.write("\t\t\t\tcase {}:\n".format(v))
            output_ori.write("\t\t\t\t\tvar res{} = new {}();\n".format(v, k))
            output_ori.write("\t\t\t\t\treturn res{};\n".format(v))
        output_def.write("\t\tpublic static readonly string {0}_NAME = \"{0}\";\n".format(k))
        output_mid.write('\t\t\t\tcase \"{}\":\n'.format(k))
        output_mid.write("\t\t\t\t\treturn {};\n".format(v))

    fout = open(out_path, 'w', encoding='UTF-8', newline='')
    final_str = CS_PROTO_FACTORY_TEMPLATE.replace('{class_id_statement}', output_parse.getvalue())
    final_str = final_str.replace('{ori_class_statement}', output_ori.getvalue())
    final_str = final_str.replace('{class_call_statement}', output_call.getvalue())
    final_str = final_str.replace('{class_def}', output_def.getvalue())
    final_str = final_str.replace('{class_mid_statement}', output_mid.getvalue())
    final_str = final_str.replace('{class_name}', class_name)
    fout.write(final_str)
    fout.close()


if __name__ == '__main__':
    load_meta('rpc_client', 'menu.txt')
    gen_proto_py('../gen/rpc_client/gen_proto_factory.py')
    print('success export gen_proto_factory.rpc_client')

    gen_proto_cs('../gen/cs/GenProtoFactory.cs', 'ProtoFactoryPb')