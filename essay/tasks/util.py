#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import random
import string

from fabric.decorators import task

__all__ = ['random_str']

KEYS = [string.lowercase,
        string.uppercase,
        string.digits,
        string.punctuation]


@task
def random_str(length=10, level=1):
    """
    生成随机字符串

    参数:
        length: 字符串长度
        level: 使用的字符集
            1 -> abcdefghijklmnopqrstuvwxyz
            2 -> abcdefghijklmnopqrstuvwxyz + ABCDEFGHIJKLMNOPQRSTUVWXYZ
            3 -> abcdefghijklmnopqrstuvwxyz + ABCDEFGHIJKLMNOPQRSTUVWXYZ + 0123456789
            4 -> abcdefghijklmnopqrstuvwxyz + ABCDEFGHIJKLMNOPQRSTUVWXYZ + 0123456789 + !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    """

    if length < 1 or 4 < level < 1:
        raise ValueError('无效参数')

    level = int(level) + 1
    keys = ''.join(KEYS[:level])

    result = ''.join([random.choice(keys) for i in range(length)])

    print result

    return result
