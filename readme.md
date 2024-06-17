# 坎巴拉太空计划模组自动翻译器

# 使用方法

1. 安装依赖
```shell
pip install -r requirements.txt
```

运行程序
```shell
python main.py -platform zhipu -token xxx -input ./input.cfg -output ./output.cfg
```

## 参数说明

**platform**

翻译平台目前支持
- zhipu: 某国内翻译平台 https://open.bigmodel.cn/

**token**

翻译平台的token

**input**

输入文件路径

**output**

输出文件路径

# 已经实现

- [x] 支持翻译cfg格式 mod的文本
- [x] 接入国内某GPT平台 提供翻译服务

# 未来规划

- [ ] 接入更多翻译引擎
- [ ] 优化翻译速度
- [ ] 优化翻译质量
- [ ] 支持更多翻译mod类型