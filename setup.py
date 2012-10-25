#!/usr/bin/env python
exec(open('hypergraph/version.py').read())
VERSION = "%s.%s.%s" % __version__[0:3]
NAME = 'hypergraph'
URL = 'http://github.com/ezod/hypergraph'
PACKAGE = 'hypergraph'

from setuptools import setup
from distutils.cmd import Command
from shutil import rmtree
import os
import sys

class GenerateDoc(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import epydoc.cli
        rmtree('doc', ignore_errors=True)
        os.mkdir('doc')
        # okay, this is a bit of a hack
        sys.argv = ['epydoc', '-v', '--name', NAME, '--url', URL, '-o', 'doc', PACKAGE]
        options, names = epydoc.cli.parse_arguments()
        epydoc.cli.main(options, names)

setup(
    name = NAME,
    version = VERSION,
    license = "LGPL",
    description = "Python module for graphs and hypergraphs.",
    author = "Aaron Mavrinac",
    author_email = "mavrin1@uwindsor.ca",
    url = URL,
    download_url = "http://github.com/downloads/ezod/hypergraph/hypergraph-%s.tar.bz2" % VERSION,
    keywords = "graph hypergraph combinatorics",
    test_suite = "test",
    cmdclass = {'doc': GenerateDoc},
)
