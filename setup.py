# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 01:47:39 2024

@author: Jose Wilson
"""

from setuptools import setup, find_packages

setup(
    name='TimeStamp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Lista de dependências do seu pacote
        'requests',
        'pandas'
        ],
    )