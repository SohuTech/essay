# coding:utf-8

__version__ = '${version}'
__git_version__ = '${git_version}'
__release_time__ = '${release_time}'

import os
from log import init_log
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

init_log()
