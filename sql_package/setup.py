# setup.py
from setuptools import setup, find_packages

setup(
    name='my_sql_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'PyQt5',
    ],
)