#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mqtt-client',
    version='1.5.0',
    description='Simple MQTT Client.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mqtt',
    author='Samuel de Ancos',
    author_email='sdeancos@gmail.com',
    url='https://github.com/sdeancos/mqtt-client',
    packages=find_packages(),
    include_package_data=False,
    python_requires='>=3.6',
    install_requires=[
        'docopt',
        'paho-mqtt',
        'terminaltables'
    ],
    entry_points={
        "console_scripts": [
            "mqtt-client = mqtt_client.__main__:main",
        ]
    },
)
