import sys

from distutils import sysconfig
from distutils.core import setup

try:
    import os
except:
    print ('')
    sys.exit(0)

setup(
    name = "aurcheck",
    author = "",
    author_email = "",
    version = "0.7.6",
    license = "GPL3",
    description = "A tool that allows to easily check updates from AUR",
    long_description = "",
    url = "http://github.com/cdede/aurcheck/",
    platforms = 'POSIX',
    packages = ['l_aurcc' ],
    data_files = [  ('share/doc/aurcheck', [ 'COPYING']),
        ],
    scripts = ['aurcheck']
)
