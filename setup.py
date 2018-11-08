#!/usr/bin/env python
import os.path
import re

from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(__file__)


def read_contents(local_filepath):
    with open(os.path.join(ROOT_DIR, local_filepath), 'rt') as f:
        return f.read()


def get_requirements(requirements_filepath):
    '''
    Return list of this package requirements via local filepath.
    '''
    requirements = []
    with open(os.path.join(ROOT_DIR, requirements_filepath), 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.rstrip()
            if not line:
                continue
            requirements.append(line)
    return requirements


def get_version(package):
    '''
    Return package version as listed in `__version__` in `init.py`.
    '''
    init_py = read_contents(os.path.join(package, '__init__.py'))
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description(markdown_filepath):
    '''
    Return the long description in RST format, when possible.
    '''
    try:
        import pypandoc
        return pypandoc.convert(markdown_filepath, 'rst')
    except ImportError:
        return read_contents(markdown_filepath)


setup(
    name='functoolsplus',
    version=get_version('functoolsplus'),
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    author='Andrzej Pragacz',
    author_email='apragacz@o2.pl',
    description='Functional programming goodies',
    license='MIT',
    keywords=' '.join((
        'functional',
        'monads',
        'functors',
        'streams',
        'immutable',
    )),
    long_description=get_long_description('README.md'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    install_requires=get_requirements(
        'requirements/requirements-base.txt'),
    python_requires='>=3.6',
    url='https://github.com/apragacz/functoolsplus',
)
