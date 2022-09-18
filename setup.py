from setuptools import setup
from glob import glob
from os.path import basename
from os.path import splitext

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]

setup(
    name="mt5_backtester",
    version="1.0.0-beta0",
    packages=['mt5_backtester'],
    install_requires = install_requires,
    description='',
    long_description=readme,
    author='RuiHirano',
    author_email='r.hrn.0930@gmail.com',
    license='MIT',
)
