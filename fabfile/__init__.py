# coding:utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

from fabric.state import env

from essay.tasks import build

env.roledefs = {
    'build': ['vagrant@127.0.0.1:2202'],
}

env.GIT_SERVER = 'https://github.com/'  # ssh地址只需要填：github.com
env.PROJECT = 'essay'
env.BUILD_PATH = '~/buildspace'
env.PROJECT_OWNER = 'SohuTech'
env.DEFAULT_BRANCH = 'master'
env.PYPI_INDEX = 'http://pypi.python.org/simple'
