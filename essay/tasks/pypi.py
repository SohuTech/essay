# coding: utf-8
from __future__ import unicode_literals

from fabric.api import run, env, task
from fabric.context_managers import settings

from essay.tasks import config

__all__ = ['sync']


@task
def sync(*packages):
    """从http://pypi.python.org同步包

    用法:
        fab pypi.sync:django==1.3,tornado
    """

    config.check('PYPI_HOST',
                 'PYPI_USER',
                 'PYPI_ROOT')

    with settings(host_string=env.PYPI_HOST, user=env.PYPI_USER):
        cmd = ["pip", "-q", "install", "--no-deps", "-i", "https://pypi.python.org/simple",
               "-d", env.PYPI_ROOT,
               ' '.join(packages)]

        run(" ".join(cmd))
