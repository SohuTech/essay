# coding:utf-8
from __future__ import unicode_literals

import posixpath
from contextlib import contextmanager
from os import path

from fabric.api import run, prompt
from fabric.contrib.files import exists
from fabric.context_managers import prefix
from fabric.state import env

from essay.tasks import process, package, fs

__all__ = []


def ensure(venv_dir, sub_dirs=None, user_mode=True):
    """
    确保虚拟环境存在

    ::
    .. _virtual environment: http://www.virtualenv.org/
    """

    if not venv_dir.startswith('/'):
        if 'VIRTUALENV_PREFIX' in env:
            venv_dir = path.join(env.VIRTUALENV_PREFIX, venv_dir)
        else:
            user_home = run('USER_HOME=$(eval echo ~${SUDO_USER}) && echo ${USER_HOME}')
            venv_dir = path.join(user_home, 'w', venv_dir)

    if is_virtualenv(venv_dir):
        return

    if package.is_virtualenv_installed_in_system():
        virtualenv_bin = 'virtualenv'
    else:
        virtualenv_bin = '~/.local/bin/virtualenv'

    command = '%(virtualenv_bin)s --quiet "%(venv_dir)s"' % locals()
    run(command)

    if not sub_dirs:
        sub_dirs = ['logs', 'etc', 'tmp']

    if 'VIRTUALENV_SUB_DIRS' in env:
        sub_dirs = list(set(sub_dirs + env.VIRTUALENV_SUB_DIRS))

    for sub_dir in sub_dirs:
        fs.ensure_dir(path.join(venv_dir, sub_dir))


@contextmanager
def activate(venv_dir, local=False):
    """
    用来启用VirtualEnv的上下文管理器

    ::
        with virtualenv('/path/to/virtualenv'):
            run('python -V')

    .. _virtual environment: http://www.virtualenv.org/
    """

    if not venv_dir.startswith('/'):
        if 'VIRTUALENV_PREFIX' in env:
            venv_dir = path.join(env.VIRTUALENV_PREFIX, venv_dir)
        else:
            user_home = run('USER_HOME=$(eval echo ~${SUDO_USER}) && echo ${USER_HOME}')
            venv_dir = path.join(user_home, 'w', venv_dir)

    if not is_virtualenv(venv_dir):
        raise Exception('无效虚拟环境: %s' % venv_dir)

    join = path.join if local else posixpath.join
    with prefix('. "%s"' % join(venv_dir, 'bin', 'activate')):
        env.CURRENT_VIRTUAL_ENV_DIR = venv_dir
        yield
        # del env['CURRENT_VIRTUAL_ENV_DIR']


def is_virtualenv(venv_dir):
    """判断指定的虚拟环境是否正确"""
    return exists(path.join(venv_dir, 'bin', 'activate'))


def remove(venv_dir):
    """删除指定的虚拟环境"""

    answer = prompt(u"确定删除虚拟环境:%s  (y/n)?" % venv_dir)
    if answer.lower() in ['y', 'yes']:
        if is_virtualenv(venv_dir):
            process.kill_by_name(path.join(venv_dir, 'bin'))
            run('rm -rf ' + venv_dir)
