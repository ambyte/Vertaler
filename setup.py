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
      data_files=[('src/icons', ['src/icons/appicons/app_icon_main.png', 'src/icons/appicons/app_icon_main24.png','src/icons/mainframe/applications-development-translation.png', 'src/icons/mainframe/document-export-2.png','src/icons/mainframe/edit-clear-2.png', 'src/icons/mainframe/edit-copy-8.png','src/icons/mainframe/edit-paste-2.png', 'src/icons/mainframe/go-next-3.png','src/icons/mainframe/kmixdocked-2.png', 'src/icons/mainframe/preferences-system-3.png','src/icons/mainframe/tools-check-spelling-32.png', 'src/icons/mainframe/view-refresh-3.png','src/icons/popupframe/ajax-loader.gif', 'src/icons/popupframe/arrow_right_12x12.png','src/icons/popupframe/checkmark_icon&16.png', 'src/icons/popupframe/clipboard_copy_icon&16.png','src/icons/popupframe/delete_icon&16.png', 'src/icons/popupframe/globe_2_icon&16.png', 'src/icons/popupframe/google_icon&16.png', 'src/icons/popupframe/home_icon&16.png', 'src/icons/popupframe/refresh_icon&16.png', 'src/icons/popupframe/sound_high_icon&16.png','src/icons/popupframe/zoom_icon&16.png']),
                  ('local', ['src/locale/ru/LC_MESSAGES/messages.mo'])],
 
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
