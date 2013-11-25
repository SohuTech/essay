# coding: utf-8

from fabric.api import parallel, task
from fabric.state import env
from essay.tasks import virtualenv, supervisor, package

__all__ = ['deploy']


@task(default=True)
@parallel(30)
def deploy(version, venv_dir, profile):
    """
    发布指定的版本

    会自动安装项目运行所需要的包
    """

    virtualenv.ensure(venv_dir)

    with virtualenv.activate(venv_dir):
        supervisor.ensure(project=env.PROJECT, profile=profile)
        package.install(env.PROJECT, version)
        supervisor.shutdown()
        supervisor.start()
