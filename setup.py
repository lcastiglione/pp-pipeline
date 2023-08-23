"""Configuración interna del paquete"""

import os
import pkg_resources
from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pipeline',
    version='0.0.3',
    author='Ing. Leonardo Castiglione',
    author_email='',
    description='Paquete con funciones para el manejo de peticiones web asíncronas, independizándose de la librería',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lcastiglione/pp-pipeline',
    project_urls={},
    license='MIT',
    packages=find_packages(exclude=["tests*", "assets*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8")
        )
    ]
)
