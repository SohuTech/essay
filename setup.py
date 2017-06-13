# coding: utf-8
from __future__ import unicode_literals

from setuptools import setup, find_packages

from essay import VERSION

setup(
    name='essay',
    version=VERSION,
    description='持续部署工具',
    long_description='',
    author='SohuTech',
    author_email='thefivefire@gmail.com',
    url='http://github.com/SohuTech/essay',
    packages=find_packages(exclude=['*.pyc']),
    include_package_data=True,
    install_requires=[
        'Fabric3',
        'Jinja2',
        ],
    entry_points={
        'console_scripts': [
            'es = essay.main:main',
            'ep = essay.main:pip_main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
