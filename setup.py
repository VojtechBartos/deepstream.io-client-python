import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('deepstream_client/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='deepstream_client',
    version=version,
    description="Python client using the dsh HTTP API",
    author="Vojtěch Bartoš",
    author_email="hi@vojtech.me",
    url="https://github.com/VojtechBartos/deepstream.io-client-python",
    packages=[
        'deepstream_client',
    ],
    include_package_data=True,
    install_requires=[
        'requests==2.18.4'
    ],
    extras_require={
        'test': [
            'py.test==3.2.3',
            'pytest-mock==1.6.3,
            'requests-mock==1.3.0'
        ],
    },
    license="MIT",
    zip_safe=False,
    platforms='any',
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
