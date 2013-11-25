#coding:utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

from fabric.state import env

from essay.tasks import build
from essay.tasks import deploy
#from essay.tasks import nginx
#from essay.tasks import supervisor

env.GIT_SERVER = 'https://github.com/'  # ssh地址只需要填：github.com

env.PROJECT = '${project_name}'
#env.BUILD_PATH = '/opt/deploy/'
#env.PROJECT_OWNER = 'EssayTech'
#env.DEFAULT_BRANCH = 'master'
#env.PYPI_INDEX = 'http://pypi.python.org/simple/'


######
# deploy settings:
env.PROCESS_COUNT = 2  #部署时启动的进程数目
env.roledefs = {
    'build': ['username@buildserverip:port'],  # 打包服务器配置
    'dev': [''],
}

env.VIRTUALENV_PREFIX = '/home/django/${project_name}'
env.SUPERVISOR_CONF_TEMPLATE = os.path.join(PROJECT_ROOT, 'conf', 'supervisord.conf')

#根据工程确定项目编号, 不同环境保证监听不同的端口，通过port参数传到supervisord.conf中。
PROJECT_NUM = 88
env.VENV_PORT_PREFIX_MAP = {
    'a': '%d0' % PROJECT_NUM,
    'b': '%d1' % PROJECT_NUM,
    'c': '%d2' % PROJECT_NUM,
    'd': '%d3' % PROJECT_NUM,
    'e': '%d4' % PROJECT_NUM,
    'f': '%d5' % PROJECT_NUM,
    'g': '%d6' % PROJECT_NUM,
    'h': '%d7' % PROJECT_NUM,
    'i': '%d8' % PROJECT_NUM,
}
