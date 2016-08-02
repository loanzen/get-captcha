#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    "requests"
]

setup(
    name='captcha',
    version='0.1.0',
    description="Get Captcha text from the image using real intelligence, not artificial intelligence.",
    long_description=readme,
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
