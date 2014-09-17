#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import os
import re
import datetime

from fabric.state import env
from fabric.api import cd, run, task, settings, roles

from essay.tasks import git, config, fs
from fabric.contrib import files
from pip.exceptions import DistributionNotFound

__all__ = ['build', 'get_latest_version', 'get_next_version']


@roles('build')  # 默认使用build role
@task(default=True)
def build(name=None, version=None, commit=None, branch=None):
    """
    打包

    参数:
        name: 描述, 如:seo。最后生成project_name-x.x.x.x-seo.tar.gz
        commit: 指定commit版本
        branch: 分支名称
        version: 自定义版本号，如果为None则根据日期生成

    commit和branch必须提供一个, 或者读取配置文件
    """

    if commit:
        check_out = commit
    elif branch:
        check_out = branch
    else:
        check_out = env.DEFAULT_BRANCH

    if not version:
        config.check('PROJECT')
        version = get_next_version(env.PROJECT)

    if name:
        version = '%s-%s' % (version, name)

    project_path = os.path.join(env.BUILD_PATH, env.PROJECT)

    if not files.exists(project_path):
        with(cd(env.BUILD_PATH)):
            git.clone('/'.join([env.PROJECT_OWNER, env.PROJECT]))

    with(cd(project_path)):
        git.checkout(check_out)
        # 在setup打包之前做进一步数据准备工作的hook
        if hasattr(env, 'PRE_BUILD_HOOK'):
            env.PRE_BUILD_HOOK()

        params = {
            'release_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'git_version': git.get_version(),
            'version': version,
        }

        fs.inplace_render(os.path.join(project_path, 'setup.py'), params)

        if hasattr(env, 'SETTINGS_BASE_FILE'):
            settings_file_path = os.path.join(project_path, *env.SETTINGS_BASE_FILE.split('/'))
            if files.exists(settings_file_path):
                fs.inplace_render(settings_file_path, params)
        else:
            settings_file_path = os.path.join(project_path, env.PROJECT, 'settings.py')
            if files.exists(settings_file_path):
                fs.inplace_render(settings_file_path, params)

            settings_dir_path = os.path.join(project_path, env.PROJECT, 'settings', '__init__.py')
            if files.exists(settings_dir_path):
                fs.inplace_render(settings_dir_path, params)

        run("python setup.py sdist upload -r internal")

@task
def get_latest_version(package_name=None):
    if not package_name:
        config.check('PROJECT')
        package_name = env.PROJECT

    # 这里直接使用了package finder，而非search command,
    # 是因为pypiserver不支持pip search
    from pip.index import PackageFinder
    from pip.req import InstallRequirement
    finder = PackageFinder(find_links=[], index_urls=[env.PYPI_INDEX])
    req = InstallRequirement(req=package_name, comes_from=None)
    try:
        url = finder.find_requirement(req, upgrade=True)
    except DistributionNotFound:
        print u'尚无任何版本！'
        return None
    filename = url.splitext()[0]
    version = re.search(r'(\d+\.?)+', filename)
    version = version.group() if version else None

    print u'当前版本: %s' % version
    return version

@task
def get_next_version(package_name=None):
    """计算下一个版本号"""

    if not package_name:
        config.check('PROJECT')
        package_name = env.PROJECT

    now = datetime.datetime.now()
    prefix = '%s.%s.%s' % (str(now.year)[-1], now.month, now.day)

    latest_version = get_latest_version(package_name)
    #如果该项目没有建立过版本,从1开始
    if not latest_version:
        index = 1
    else:
        last_prefix, last_index = latest_version.rsplit('.', 1)

        if last_prefix != prefix:
            index = 1
        else:
            index = int(last_index) + 1

    version = prefix + '.' + str(index)
    print u'下一个版本: ' + version

    return version
