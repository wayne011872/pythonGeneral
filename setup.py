from setuptools import find_packages, setup

setup(
    name="pythonGeneral",
    version="1.3.0",
    packages = find_packages(),
    install_requires = [
        'pymongo',
        'pandas'
    ],
)
