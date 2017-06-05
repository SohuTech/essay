# coding: utf-8
from __future__ import unicode_literals, print_function

from fabric.api import task
from fabric.state import env
from fabric.network import parse_host_string

from essay.utils import import_by_path


__all__ = ['validate']


class Validator(object):
    def __init__(self, venv, role, *args, **kwargs):
        self.venv = venv
        self.role = role
        self.args = args
        self.kwargs = kwargs

    def run(self):
        hosts = self.get_hosts()
        ports = self.get_ports()

        result = True
        for host in hosts:
            for port in ports:
                result = self.validate(host, port)
                if not result:
                    print("验证失败: 主机[{}] 端口[{}]".format(host, port))
        if result:
            print("验证成功")

    def validate(self, host, port):
        """
        验证服务可用性

        子类重载此函数，并返回True或False
        """
        raise NotImplementedError

    def get_hosts(self):
        return [
            parse_host_string(host_string)['host']
            for host_string in env.roledefs[self.role]
        ]

    def get_ports(self):
        port_prefix = env.VENV_PORT_PREFIX_MAP[self.venv]
        return [
            int(str(port_prefix) + str(port_suffix))
            for port_suffix in range(env.PROCESS_COUNT)
        ]


@task
def validate(venv, role='product', *args, **kwargs):
    """
    验证部署是否成功

    参数:
        venv: 虚拟环境名称
        role: 服务器角色

    用法:
        $ fab validate:a,product,[custom_args]

    """
    validator_path = env.VALIDATOR_CLASS
    validator_class = import_by_path(validator_path)

    try:
        validator_instance = validator_class(venv, role, *args, **kwargs)
    except:
        raise Exception("{}不是一个有效的Validator".format(validator_path))

    validator_instance.run()
