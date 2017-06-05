# coding: utf-8
from __future__ import unicode_literals, print_function
from os import path

from fabric.api import task
from fabric.state import env
from fabric.contrib import files


def check(*properties):
    def _check(_property):
        if not hasattr(env, _property):
            msg = 'env has not attribute [{}]'.format(_property)
            print(msg)
            raise Exception(msg)

    for property in properties:
        _check(property)


@task(default=True)
def upload_conf(**context):
    if hasattr(env, 'LOCAL_SERVER_CONF'):
        for local_conf, server_conf in env.LOCAL_SERVER_CONF:
            template_dir, filename = path.dirname(local_conf), path.basename(local_conf)
            venv_dir = env.CURRENT_VIRTUAL_ENV_DIR
            destination = path.join(venv_dir, server_conf)

            files.upload_template(filename, destination, context=context, use_jinja=True, template_dir=template_dir)
    else:
        print('no local conf to upload')
