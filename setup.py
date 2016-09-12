#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    "requests",
    "retrying"
]

setup(
    name='get-captcha',
    version='0.2.0',
    description="Get Captcha text from the image using real intelligence, not artificial intelligence. Its a client for get-captcha apis",
    long_description='',
    author="Suraj Arya",
    author_email='suraj@loanzen.in',
    url='https://github.com/suraj-arya/captcha',
    packages=[
        'captcha',
    ],
    package_dir={'captcha':
                 'captcha'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
