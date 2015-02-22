import os

from setuptools import setup

setup(name='scriptlib',
    version='0.1',
    description='Some lib to create script',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    author='Xavier Fernandez',
    author_email='xav.fernandez@gmail.com',
    url='http://github.com/xavfernandez/scriptlib/',
    keywords='packaging script',
    license='MIT',
    packages=['scriptlib'],
    include_package_data=True,
)

