from setuptools import find_packages, setup

setup(
    name="pythonGeneral",
    version="0.1.0",
    packages = find_packages(),
    install_requires = [
        'pymongo',
        'pandas'
    ],
)