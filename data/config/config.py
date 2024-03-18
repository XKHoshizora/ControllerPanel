# 该模块用于配置

import json
from _version import __version__


# 读取 json 配置文件
def loads_cfg(file_name='config.json'):
    return json.loads(open(file_name, mode='r+', encoding='utf-8').read())


# 写入 json 配置文件
def dumps_cfg(file_name='config.json', **kwargs):
    return open(file_name, mode='w+', encoding='utf-8').write(json.dumps(kwargs))


# 读取默认 json 配置文件
def default_cfg(file_name='default_config.json'):
    return json.loads(open(file_name, mode='r', encoding='utf-8').read())


# 配置类
class Config:
    cfg = {
        'author': 'ZhuLab @SUN YIBO',
        'version': __version__,  # version
        'constant': {  # 常数

        },
        'ui': {  # 界面设置
            'full_window': True,
        },
        'D': {},
    }

    def __init__(self):
        pass

    def configure(self):
        pass


if __name__ == '__main__':
    print(loads_cfg())
