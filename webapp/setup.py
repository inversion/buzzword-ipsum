from setuptools import setup, find_packages

import buzzwordipsum

setup(
    name = 'buzzwordipsum',
    version = buzzwordipsum.__version__,
    packages = find_packages(),
    url = 'https://github.com/inversion/buzzword-ipsum',
)

