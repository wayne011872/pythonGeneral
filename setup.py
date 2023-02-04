from setuptools import find_packages, setup

setup(
    name="pythonGeneral",
    version="1.0.0",
    packages = find_packages(),
    install_requires = [
        'pymongo',
        'pandas',
        'bs4',
        'openpyxl',
        'fake-useragent',
        'requests',
        'urllib3'
    ],
)
