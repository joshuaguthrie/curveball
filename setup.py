#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of curveball.
# https://github.com/yoavram/curveball

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>

from setuptools import setup, find_packages
import os
import versioneer

with open('README.md') as f:
    README = f.read()

setup(
    name='curveball',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Predicting competition results from growth curves',
    long_description=README,
    keywords='microbiology biomath evolution',
    author='Yoav Ram',
    author_email='yoav@yoavram.com',
    url='https://github.com/yoavram/curveball',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    data_files=[('data', ['data/Tecan_280715.xlsx', 'data/Tecan_210115.xlsx', 'data/Tecan_210115.csv', 'data/20130211_dh.zip', 'data/plate_9_OD.mat', 'data/Sunrise_180515_0916.xlsx']),
                  ('plate_templates', ['plate_templates/checkerboard.csv', 'plate_templates/G-RG-R.csv']),
    ],
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        # click, numpy, scipy, pyparsing, pytz, six, python-dateutil, matplotlib, pandas, statsmodels, lxml, seaborn, sympy, xlrd, future, lmfit
        'future',
        'click',
        'python-dateutil',
        'lxml',
        'xlrd',
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
        'seaborn',
        'statsmodels',
        'sympy',
        'lmfit>=0.9.0',
    ],
    extras_require={
        'tests': [
            'nose',
            'coverage',
            'pillow'
        ],
        'docs': [
            'sphinx>=1.3.0',
            'numpydoc'
        ]
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'curveball=curveball.scripts.cli:cli',
        ],
    },
)
