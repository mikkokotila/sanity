#! /usr/bin/env python
#
# Copyright (C) 2019 Mikko Kotila

DESCRIPTION = "Programmatic Media Investment Simulator"
LONG_DESCRIPTION = """\
Sanity is a tool for intelligent media buying. It brings sanity to the process
by helping you to first check if your media investment plan makes any sense in
the first place. The approach is 100% based on available research and data.
"""

DISTNAME = 'sanity'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://nearfuturetoday.com'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/mikkokotila/sanity/'
VERSION = '0.0.2'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

install_requires = ['dedomena',
                    'numpy',
                    'pandas']


if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=install_requires,
          packages=['sanity'],

          classifiers=['Intended Audience :: Science/Research',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6',
                       'License :: OSI Approved :: MIT License',
                       'Topic :: Scientific/Engineering :: Human Machine Interfaces',
                       'Topic :: Scientific/Engineering :: Information Analysis',
                       'Topic :: Scientific/Engineering :: Mathematics',
                       'Operating System :: POSIX',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Operating System :: Microsoft :: Windows :: Windows 10'])
