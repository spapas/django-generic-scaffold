#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-generic-scaffold',
    version='0.1.1',
    description='Generic scaffolding for Django',

    author='Serafeim Papastefanos',
    author_email='spapas@gmail.com',
    license='MIT',
    url='https://github.com/spapas/django-generic-scaffold/',
    zip_safe=False,
    include_package_data=False,
    packages=find_packages(exclude=['tests.*', 'tests',]),

    install_requires=['Django >=1.4', 'six'],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
