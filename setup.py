from setuptools import setup, find_packages
import os

version = os.environ['VERSION']

setup(
    name='balderdash',
    version=version,
    description='Builders for monitoring dashboards',
    url='http://github.com/daviddenton/balderdash/',
    license='Apache 2.0',
    author='daviddenton',
    author_email='denton.david+pypy@gmail.com',
    packages=find_packages(exclude=['tests*']),
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)