# coding: utf-8
import os
from fabric.state import env


def install(args):
    cmd = 'pip install -i=%s %s' % (env.PYPI_INDEX, ' '.join(args))
    os.system(cmd)


def default(args):
    cmd = 'pip ' + ' '.join(args)
    os.system(cmd)
