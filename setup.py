#!/usr/bin/env python
""" Setup file for Vertaler package """
 
from distutils.core import setup
setup(name='vertaler',
      version='0.1',
      description='Vertaler',
      long_description = "Translator for your application",
      author='Sergey Gulyaev',
      author_email='astraway@gmail.com',
      url='http://vertalerproject.org/',
      packages=[ 'src','src.controllers','src.modules','src.views' ],
      scripts=['Vertaler.py'],
 
      classifiers=(
          'Development Status :: 5 - Production/Stable',
          'Environment :: X11 Applications',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
        ),
      license="GPL-2"
     )