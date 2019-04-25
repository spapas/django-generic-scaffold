#!/usr/bin/env python
from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='django-generic-scaffold',
    version='0.5.4',
    description='Generic scaffolding for Django',
    long_description=readme(),
    author='Serafeim Papastefanos',
    author_email='spapas@gmail.com',
    license='MIT',
    url='https://github.com/spapas/django-generic-scaffold/',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['tests.*', 'tests',]),

    install_requires=['Django >=1.8', 'six'],

    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
