from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

import buzzwordipsum

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--cov', 'buzzwordipsum', '--cov-report', 'term-missing']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name = 'buzzwordipsum',
    version = buzzwordipsum.__version__,
    packages = find_packages(),

    install_requires = ['Flask>=0.10.1', 'Flask-RESTful>=0.2.11', 'Pattern>=2.6'],
    tests_require = ['pytest>=1.4.20', 'pytest-cov>=1.6'],
    cmdclass={'test': PyTest},

    url = 'https://github.com/inversion/buzzword-ipsum',
)

