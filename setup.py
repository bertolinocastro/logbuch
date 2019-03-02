from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

# auto setting bash completion var in user's .bashrc if it's not already set


class PostInstall(install):
    def run(self):
        cont = ''
        cmd = 'eval "$(_LOGBUCH_COMPLETE=source logbuch)"'
        if sys.platform.startswith('linux'):
            with open(os.path.expanduser('~/.bashrc'), 'r') as f:
                s = f.read()
            if not cmd in s:
                with open(os.path.expanduser('~/.bashrc'), 'a+') as f:
                    f.write("\n%s\n%s\n\n" % ('# added by Logbuch installer', cmd))
        install.run(self)


setup(
    name='logbuch',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'whichcraft',
    ],
    entry_points='''
        [console_scripts]
        logbuch=logbuch.src.main:cli
    ''',
    python_requires='>=3.7',
    cmdclass={'install': PostInstall},
)
