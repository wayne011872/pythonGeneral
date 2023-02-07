from setuptools import find_packages, setup

setup(
    name="pythonGeneral",
    version="1.4.0",
    packages = find_packages(),
    install_requires = [
        'pymongo',
        'pandas'
    ],
)
