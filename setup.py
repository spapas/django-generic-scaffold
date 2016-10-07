#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-generic-scaffold',
    version='0.4.0',
    description='Generic scaffolding for Django',

    author='Serafeim Papastefanos',
    author_email='spapas@gmail.com',
    license='MIT',
    url='https://github.com/spapas/django-generic-scaffold/',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['tests.*', 'tests',]),

    install_requires=['Django >=1.6', 'six'],

    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
