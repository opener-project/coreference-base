# coding=utf-8
from distutils.core import setup

setup(
    name='corefgraph',
    version='0.9.0',
    author='Josu Bermúdez <josu.bermudez@deusto.es>, Rodrigo Agerri <rodrigo.agerri@ehu.es>',
    author_email='rodrigo.agerri@ehu.es',
    packages=['corefgraph'],
    url='https://github.com/opener-project/coreference-base',
    description='Coreference resolution',
    long_description=open('README.md').read(),
    install_requires=['networkx','pyYAML'],
)
