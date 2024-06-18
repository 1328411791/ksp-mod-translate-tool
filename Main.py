import argparse
import re
import time
from tqdm import tqdm
import time

from tools.Youdao import Youdao
from tools.ZhipuTool import ZhipuTool

global translationTools


def init_output_file(output):
    output.writelines("Localization\n")
    output.writelines("{\n")
    output.write("\t zh-cn\n")
    output.writelines("\t{\n")


def close_output_file(output):
    output.writelines("\t}\n")
    output.writelines("}\n")


def escape_special_chars(text):
    special_chars = ['\n', '\t', '\r', '\b', '\f', '\v']
    for char in special_chars:
        if char in text:
            text = text.replace(char, '\\' + char.strip('\\'))
    return text


def read_cfg_file(input_file_path,output_file_path):
    # 匹配 #开头 中间有=号的行
    word = re.compile("#.*=.*")
    # 注释的正则
    annotation = re.compile("//.*")

    with open(output_file_path, "w", encoding="utf-8") as output:
        init_output_file(output)
        with open(input_file_path, "r") as f:
            lines = f.readlines()
            pbar = tqdm(total=len(lines))
            for index, line in enumerate(lines):
                pbar.update(1)

                # 如果是注释行
                if annotation.findall(line):
                    # print("annotation ", line)
                    output.writelines(line)
                elif line == '\n':
                    output.writelines(line)
                elif word.findall(line):
                    # 匹配到的行
                    # print("text line ", line)
                    # =分割字符串
                    split = line.split("=")
                    # 翻译
                    respond = translationTools.translate_word(split[1])
                    respond = escape_special_chars(respond)
                    if respond is None:
                        respond = split[1]
                    # 替换
                    line = line.replace(split[1], respond)
                    # print("output line ", line)
                    # 写入文件
                    output.writelines(line)
                    output.write("\n")

        close_output_file(output)


if __name__ == "__main__":

    # 识别命令行参数 -p -
    parser = argparse.ArgumentParser()
    parser.add_argument('-token', type=str, help='token parameter')
    parser.add_argument('-app_secret', type=str, help='platform parameter')
    parser.add_argument('-app_key', type=str, help='platform parameter')
    parser.add_argument('-platform', type=str, help='platform parameter',default="zhipu")
    parser.add_argument('-output', type=str, help='output parameter',default= "./zh-cn.cfg")
    parser.add_argument('-input', type=str, help='input parameter',default= "./en-us.cfg")

    args = parser.parse_args()

    token = args.token
    translation_way = args.platform
    output = args.output
    input = args.input
    app_key = args.app_key
    app_secret = args.app_secret

    print("translation_way:", translation_way)
    print("token:", token)
    print("input path:", input)
    print("output path:", output)

    if translation_way == "zhipu":
        translationTools = ZhipuTool(token)
    elif translation_way == "youdao":
        translationTools = Youdao(app_key=app_key, app_secret=app_secret)

    # wait for 5 seconds
    print("选择完成，等待5秒后开始翻译...")
    time.sleep(5)

    read_cfg_file(input, output)

    print("done")
