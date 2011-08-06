#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Lettuce Web',
    version='0.1',
    description='Behavior Driven Development (BDD) '\
                'abstract web driver for lettuce',
    long_description=open('README').read(),
    # Get more strings from
    # http://www.python.org/pypi?:action=list_classifiers
    author='Max Klymyshyn',
    author_email='klymyshyn@gmail.com',
    url='https://github.com/joymax/lettuce-web',
    download_url='https://github.com/joymax/lettuce-web/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    tests_require=[
        'lettuce',
        'lxml',
        'fudge',
    ],
    install_requires=[
       'lettuce',
       'lxml'
    ],
    test_suite='lettuce_web.runtests',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
