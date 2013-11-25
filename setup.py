# coding: utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='essay',
    version='${version}',
    description=u'持续部署工具',
    long_description='',
    author='SohuTech',
    author_email='thefivefire@gmail.com',
    url='http://github.com/SohuTech/essay',
    packages=find_packages(exclude=['*.pyc']),
    include_package_data=True,
    install_requires=[
        'Fabric',
        'Jinja2',
        ],
    entry_points={
        'console_scripts': [
            'es = essay.main:main',
            'ep = essay.main:pip_main',
        ]
    },
)
