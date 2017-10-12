import re
import ast
from setuptools import setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("deepstream_client/__init__.py", "rb") as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode("utf-8")).group(1)))

setup(
    name="deepstream_client",
    version=version,
    license="MIT",
    description="Python client using the dsh HTTP API",
    author="Vojtech Bartos",
    author_email="hi@vojtech.me",
    url="https://github.com/VojtechBartos/deepstream.io-client-python",
    platforms="any",
    keywords=["deepstream"],
    packages=[
        "deepstream_client",
    ],
    include_package_data=True,
    install_requires=[
        "requests==2.18.4"
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        "pytest==3.2.3",
        "pytest-mock==1.6.3",
        "requests-mock==1.3.0"
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
