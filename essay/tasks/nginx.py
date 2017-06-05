#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from fabric.api import run, env, sudo
from fabric.contrib import files
from fabric.decorators import task

from essay.tasks import config


def _nginx_command(command, nginx_bin=None, nginx_conf=None, use_sudo=False):
    if not nginx_bin:
        config.check('NGINX_BIN')
        nginx_bin = env.NGINX_BIN

    if not nginx_conf:
        config.check('NGINX_CONF')
        nginx_conf = env.NGINX_CONF

    if command == 'start':
        cmd = '%(nginx_bin)s -c %(nginx_conf)s' % locals()
    else:
        cmd = '%(nginx_bin)s -c %(nginx_conf)s -s %(command)s' % locals()

    if use_sudo:
        sudo(cmd)
    else:
        run(cmd)


@task
def stop(nginx_bin=None, nginx_conf=None, use_sudo=False):
    """
    停止Nginx

    参数:
        nginx_bin: nginx可执行文件路径，如果为提供则从env获取。
        nginx_conf: nginx配置文件路径，如果为提供则从env获取。
    """

    _nginx_command('stop', nginx_bin, nginx_conf, use_sudo=use_sudo)


@task
def start(nginx_bin=None, nginx_conf=None, use_sudo=False):
    """
    启动Nginx

    参数:
        nginx_bin: nginx可执行文件路径，如果为提供则从env获取。
        nginx_conf: nginx配置文件路径，如果为提供则从env获取。
    """

    _nginx_command('start', nginx_bin, nginx_conf, use_sudo=use_sudo)


@task
def reload(nginx_bin=None, nginx_conf=None, use_sudo=False):
    """
    重启Nginx

    参数:
        nginx_bin: nginx可执行文件路径，如果为提供则从env获取。
        nginx_conf: nginx配置文件路径，如果为提供则从env获取。
    """
    _nginx_command('reload', nginx_bin, nginx_conf, use_sudo=use_sudo)


@task
def switch(src_pattern, dst_pattern, root=None, nginx_bin=None, nginx_conf=None):
    """
    修改配置文件并重启：源文本,目标文本,[root]（使用root)

    主要用于AB环境的切换，将配置文件中的src_pattern修改为dst_pattern，并重启。

    参数:
        src_pattern: 源模式，如upstreamA
        src_pattern: 目标模式，如upstreamB
        nginx_bin: nginx可执行文件路径，如果为提供则从env获取。
        nginx_conf: nginx配置文件路径，如果为提供则从env获取。
    """

    if not nginx_conf:
        config.check('NGINX_CONF')
        nginx_conf = env.NGINX_CONF

    use_sudo = (root == 'root')
    files.sed(nginx_conf, src_pattern, dst_pattern, use_sudo=use_sudo)
    reload(nginx_bin, nginx_conf, use_sudo=use_sudo)
