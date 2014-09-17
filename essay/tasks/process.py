# coding:utf-8
from __future__ import unicode_literals

from fabric.api import run
from fabric.context_managers import settings, hide
from fabric.decorators import task


@task
def kill_by_name(name):
    """
    停止指定特征的进程
    """

    with settings(warn_only=True):
        run("ps aux | grep '%s' | grep -v 'grep' | awk '{print $2}' | xargs kill -9" % name)


@task
def top():
    """
    查看系统负载
    """

    run("top -b | head -n 1")


@task
def ps_by_venv(venv_dir):
    """"
    查看指定虚拟环境的进程CPU占用
    """

    with hide('status', 'running', 'stderr'):
        run("""ps aux | grep -v grep | grep -v supervisor | grep %s | awk '{print $3, "|", $4}'""" % venv_dir)
