# coding: utf-8
from __future__ import unicode_literals

from fabric.api import run, env
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.decorators import task

__all__ = ['install']


def is_virtualenv_installed_in_system():
    """
    检查virtualenv是否在系统目录安装
    """

    with settings(warn_only=True):
        return 'no virtualenv' not in run('which virtualenv') or \
            'which' not in run('which virtualenv')


def is_virtualenv_installed_in_user():
    """
    检查virtualenv是否在系统目录安装
    """

    with settings(warn_only=True):
        return exists('~/.local/bin/virtualenv')


def is_virtualenv_installed():
    """
    检查virtualenv是否已安装
    """

    return is_virtualenv_installed_in_system() or is_virtualenv_installed_in_user()


def is_installed(package):
    """检查Python包是否被安装

    注意：只能在虚拟Python环境中执行
    """

    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')
    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR

    with settings(warn_only=True):
        res = run('%(venv_dir)s/bin/pip freeze' % locals())
    packages = [line.split('==')[0].lower() for line in res.splitlines()]

    return package.lower() in packages


@task
def install(package_name, version=None, private=True, user_mode=True):
    """
    用Pip安装Python包

    参数:
        package: 包名，可以指定版本，如Fabric==1.4.3
        private: 利用私有PYPI安装
        user_mode: 安装在用户目录

    注意：只能在虚拟Python环境中执行
    """

    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')

    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR

    options = []

    if hasattr(env, 'HTTP_PROXY'):
        options.append('--proxy=' + env.HTTP_PROXY)

    if private:
        options.append('-i ' + env.PYPI_INDEX)

    options_str = ' '.join(options)
    if version:
        package_name += '==' + version

    command = '%(venv_dir)s/bin/pip install %(options_str)s %(package_name)s' % locals()

    run(command)


def ensure(package, private=True, user_mode=True):
    """检查Python包有没有被安装，如果没有则安装

    注意：只能在虚拟Python环境中执行
    """

    if not is_installed(package):
        install(package, private=private, user_mode=user_mode)


def uninstall(package):
    """卸载Python包

    注意：只能在虚拟Python环境中执行
    """

    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')

    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR
    run("%(venv_dir)s/bin/pip uninstall -y %(package)s" % locals())
