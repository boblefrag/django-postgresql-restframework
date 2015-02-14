# -*- coding: utf-8 -*-
"""Python packaging."""
from os.path import join, dirname, abspath
import sys

from setuptools import setup


#: Absolute path to directory containing setup.py file.
ROOT = dirname(abspath(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2


def read_relative_file(filename):
    """Returns contents of the given file, whose path is supposed relative
    to this module."""
    with open(join(ROOT, filename)) as f:
        return f.read()


# Data for use in setup.
NAME = 'postgresql_restframework'
DESCRIPTION = 'django-restframework with native Postgresql Json support'
README = read_relative_file('README.rst').strip()
__VERSION__ = read_relative_file('VERSION').strip()
AUTHOR = u'Yohann Gabory'
EMAIL = 'yohann@gabory.fr'
LICENSE = 'MIT'
URL = 'https://github.com/boblefrag/django-postgresql-restframework/'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: MIT',
    'Programming Language :: Python :: 2.7',
]
KEYWORDS = []
PACKAGES = [NAME.replace('-', '_')]
REQUIREMENTS = [
    "Django",
    "djangorestframework"

]
TEST_REQUIREMENTS = ['django-nose==1.2, coverage==3.7.1']
params = dict(
    name=NAME,
    version=__VERSION__,
    description=DESCRIPTION,
    long_description=README,
    classifiers=CLASSIFIERS,
    keywords=' '.join(KEYWORDS),
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=REQUIREMENTS
)

if __name__ == '__main__':
    setup(**params)
