# coding: utf-8
from __future__ import unicode_literals

from importlib import import_module


def import_by_path(dotted_path):
    """
    根据路径动态引入模块属性
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise Exception('%s不是一个有效的模块路径' % module_path)

    try:
        module = import_module(module_path)
    except ImportError as e:
        raise Exception('模块引入错误: "%s"' % e)

    try:
        attr = getattr(module, class_name)
    except AttributeError as e:
        raise Exception('模块引入错误: "%s"' % e)

    return attr
