# coding: utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README').read()

setup(
    name='${project_name}',
    version='${version}',
    description='',
    long_description=readme,
    author='',
    author_email='',
    url='http://www.sohu.com',
    packages=find_packages(exclude=['*.pyc']),
    include_package_data = True,
    package_data = {
    },
    install_requires=[
        'django>1.3',
        'gunicorn',
        ],
    entry_points={
        'console_scripts': [
            '${project_name} = ${project_name}.main:main',
        ]
    },
)
