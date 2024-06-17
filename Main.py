import argparse
import re
import time

from tools.ZhipuTool import ZhipuTool

global translationTools


def init_output_file(output):
    output.writelines("Localization\n")
    output.writelines("{\n")
    output.write("\t zh-ch\n")
    output.writelines("\t{\n")


def close_output_file(output):
    output.writelines("\t}\n")
    output.writelines("}\n")


def escape_special_chars(text):
    special_chars = ['\n', '\t', '\r', '\b', '\f', '\v', '\\', '\"', '\'']
    for char in special_chars:
        if char in text:
            text = text.replace(char, '\\' + char.strip('\\'))
    return text


def read_cfg_file(input_file_path,output_file_path):
    # 匹配 #开头 中间有=号的行
    re_compile = re.compile("#.*=.*")

    with open(output_file_path, "w", encoding="utf-8") as output:
        init_output_file(output)
        with open(input_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                # 正则表达式匹配
                match = re_compile.findall(line)
                if match:
                    # 匹配到的行
                    print("read line ", line)
                    # =分割字符串
                    split = line.split("=")
                    # 翻译
                    respond = translationTools.translate_word(split[1])
                    respond = escape_special_chars(respond)
                    if respond is None:
                        respond = split[1]
                    # 替换
                    line = line.replace(split[1], respond)
                    print("output line ", line)
                    # 写入文件
                    output.writelines(line)
                    output.write("\n")
        close_output_file(output)


if __name__ == "__main__":

    # 识别命令行参数 -p -
    parser = argparse.ArgumentParser()
    parser.add_argument('-token', type=str, help='token parameter')
    parser.add_argument('-platform', type=str, help='platform parameter')
    parser.add_argument('-output', type=str, help='output parameter')
    parser.add_argument('-input', type=str, help='input parameter')

    args = parser.parse_args()

    token = args.token
    translation_way = args.platform
    output = args.output
    input = args.input

    print("translation_way:", translation_way)
    print("token:", token)
    print("input path:", input)
    print("output path:", output)

    if translation_way == "zhipu":
        translationTools = ZhipuTool(token)

    # wait for 5 seconds
    print("选择完成，等待5秒后开始翻译...")
    time.sleep(5)

    read_cfg_file(input, output)

    print("done")
