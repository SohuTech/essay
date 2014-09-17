# coding: utf-8
from __future__ import unicode_literals

from fabric.api import parallel, task
from fabric.state import env

from essay.tasks import virtualenv, supervisor, package, build

__all__ = ['deploy', 'quickdeploy']


@task(default=True)
@parallel(30)
def deploy(version, venv_dir, profile):
    """
    发布指定的版本

    会自动安装项目运行所需要的包
    """

    if not version:
        version = build.get_latest_version()

    virtualenv.ensure(venv_dir)

    with virtualenv.activate(venv_dir):
        supervisor.ensure(project=env.PROJECT, profile=profile)
        package.install(env.PROJECT, version)
        supervisor.shutdown()
        supervisor.start()


@task(default=True)
def quickdeploy(venv_dir, profile, branch=None):
    """
    快速部署

        $ fab -R yourroles quickdeploy:a,test,master
    """

    deploy_host_string = env.host_string

    build_host = env.roledefs.get('build')
    env.host_string = build_host[0] if isinstance(build_host, list) else build_host
    build.build(branch=branch)

    env.host_string = deploy_host_string
    version = build.get_latest_version()

    deploy(version, venv_dir, profile)
