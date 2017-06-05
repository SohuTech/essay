# coding:utf-8
from __future__ import unicode_literals

from os import path

from fabric.api import run, settings
from fabric.context_managers import cd
from fabric.contrib import files
from fabric.decorators import task
from fabric.state import env

from essay.tasks import config, util, virtualenv, package

__all__ = ['start_process', 'stop_process', 'restart_process', 'reload']


def ensure(**context):
    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')
    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR

    package.ensure('supervisor')

    context.setdefault('run_root', venv_dir)
    context.setdefault('username', util.random_str(10))
    context.setdefault('password', util.random_str(20, True))
    context.setdefault('process_count', 2)
    context.setdefault('venv_dir', venv_dir)
    context.setdefault('virtualenv_name', venv_dir[-1:])
    if 'VENV_PORT_PREFIX_MAP' in env and isinstance(env.VENV_PORT_PREFIX_MAP, dict):
        try:
            context.setdefault('port', env.VENV_PORT_PREFIX_MAP[venv_dir[-1:]])
        except KeyError:
            raise Exception('你的端口配置VENV_DIR_PORT_MAP中key[%s]不存在!' % venv_dir[-1:])
    if 'PROCESS_COUNT' in env:
        context['process_count'] = env.PROCESS_COUNT
    config.check('SUPERVISOR_CONF_TEMPLATE')
    config_template = env.SUPERVISOR_CONF_TEMPLATE
    destination = path.join(venv_dir, 'etc', 'supervisord.conf')

    template_dir, filename = path.dirname(config_template), path.basename(config_template)

    files.upload_template(filename, destination, context=context, use_jinja=True, template_dir=template_dir)


def _supervisor_command(command, venv_dir=None):
    if venv_dir:
        with virtualenv.activate(venv_dir):
            _supervisor_command(command)

    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')

    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR

    # 停止supervisor管理的进程
    with settings(warn_only=True), cd(venv_dir):
        run('bin/supervisorctl -c etc/supervisord.conf ' + command)


@task
def start(venv_dir=None):
    """重启指定虚拟环境的supervisor"""

    if venv_dir:
        with virtualenv.activate(venv_dir):
            start()

    if 'CURRENT_VIRTUAL_ENV_DIR' not in env:
        raise Exception('只可以在虚拟环境安装Python包')

    venv_dir = env.CURRENT_VIRTUAL_ENV_DIR

    with settings(warn_only=True), cd(venv_dir):
        # 停止supervisor管理的进程
        run('bin/supervisord -c etc/supervisord.conf ')


@task
def shutdown(venv_dir=None):
    """重启指定虚拟环境的supervisor"""

    _supervisor_command('shutdown', venv_dir)


@task
def reload(venv_dir=None):
    """重启指定虚拟环境的supervisor"""

    _supervisor_command('reload', venv_dir)


@task
def start_process(name, venv_dir=None):
    """
    启动进程
    """

    _supervisor_command(' start ' + name, venv_dir)


@task
def stop_process(name, venv_dir=None):
    """
    关闭进程
    """

    _supervisor_command(' stop ' + name, venv_dir)


@task
def restart_process(name, venv_dir=None):
    """
    重启进程
    """

    _supervisor_command(' restart ' + name, venv_dir)
