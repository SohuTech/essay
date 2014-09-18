# coding: utf-8
from __future__ import unicode_literals
import os
from os import path

from fabric.contrib import files
from fabric.decorators import task
from fabric.operations import run, local

__all__ = ['rm_by_pattern']

KERNEL_NAME = os.uname()[0].lower()


def ensure_dir(dir, in_local=False):
    """确保指定的dir被创建"""

    if in_local:
        if not path.isdir(dir):
            local("mkdir -p " + dir)
    elif not files.exists(dir):
        run("mkdir -p " + dir)


def remove_dir(dir, in_local=False):
    """删除指定的文件夹"""

    if in_local:
        if not path.isdir(dir):
            local("rm -r " + dir)
    elif not files.exists(dir):
        run("rm -r " + dir)


@task
def rm_by_pattern(directory, pattern, in_local=False):
    """
    删除指定格式的文件

    参数:
        directory: 目录
        pattern: 格式
        in_local: 在本地执行（默认）

    示例:
        fab fs.rm_by_pattern:.,.pyc,True
    """

    if in_local:
        local('find %s |grep %s | xargs rm -rf' % (directory, pattern))
    else:
        run('find %s |grep %s | xargs rm -rf' % (directory, pattern))


def inplace_render(filename, params):
    for key, value in params.items():
        files.sed(filename, '\$\{%s\}' % key, value)
