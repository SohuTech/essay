# coding: utf-8

"""
创建新工程结构
"""

import os
import string
import logging
from os import path

from fabric.api import lcd
from fabric.operations import prompt

from essay import settings
from essay.tasks import fs
from essay.tasks import git

logger = logging.getLogger(__name__)


def create_project(project, template='default'):
    """创建本地工程"""
    init_project(project, template)
    with lcd(project):
        git.command('git init', in_local=True)
        git.add(add_all=True, in_local=True)
        git.commit(u'初始化工程结构', in_local=True)
        repos = prompt('请输入Git仓库地址:')
        if repos:
            git.command('git remote add origin %s' % repos, in_local=True)
            git.command('git push -u origin master', in_local=True)


def init_project(project, template='default'):
    """初始化本地项目

    此方法不需要连接git服务器
    """
    if project is None:
        project_dir = path.abspath('.') 
        template = 'init'
        project = ''
        params = {
            'project_name': project
        }
    else:
        project_dir = path.abspath(project)
        fs.ensure_dir(project, in_local=True)

        params = {
            'project_name': project
        }

    build_structure(project, project_dir, params, template)


def build_structure(project, dst, params, template='default'):
    """
        拷贝工程打包及fab文件到工程
    """
    dst = dst.rstrip('/')

    template_dir = path.join(settings.PROJECT_ROOT, 'templates', template)
    for root, dirs, files in os.walk(template_dir):
        for name in files:
            if name.endswith('.tpl'):
                src = path.join(root, name)
                dst_filename = src.replace(template_dir, dst).rstrip('.tpl').replace('__project__', project)
                dst_dir = os.path.dirname(dst_filename)

                fs.ensure_dir(dst_dir, in_local=True)

                content = open(src).read().decode('utf-8')
                if not name.endswith('.conf.tpl'):
                    content = string.Template(content).safe_substitute(**params)

                open(dst_filename, 'w').write(content.encode('utf-8'))
