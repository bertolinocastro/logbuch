import sys
import subprocess
import os
import re

class Config(object):
    _base = '~/.logbuch'
    _confF = 'conf.cfg'
    _content =  "PROJECTS_FOLDER=%s\n"+\
                "ACTIVE_PROJECT=%s\n"+\
                "EDITOR=%s\n"

    _PROJS_FOLD = ''
    _ACT_PROJ = ''
    _EDITOR = ''

    def __init__(self):
        self._base = os.path.expanduser(self._base)
        self.confOpen()

    def confOpen(self):
        if not os.path.exists(self._base):
            os.mkdir(self._base)

        content = ''
        if os.path.exists(self._base+'/'+self._confF):
            with open(self._base+'/'+self._confF, 'a+') as f:
                f.seek(0)
                content = f.read()
        # ----

        # running default configuration
        if not content:
            print('There is no configuration file in the system. Creating: %s'%self._base+'/'+self._confF)
            content = self._content%(
                os.path.expanduser('~/logbuch_projects'),
                'default', 'vi')
            with open(self._base+'/'+self._confF,'w') as f:
                f.write(content)
        # ---

        try:
            self._PROJS_FOLD = re.findall('PROJECTS_FOLDER\s*=\s*(.+)', content)[0]
            self._ACT_PROJ = re.findall('ACTIVE_PROJECT\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: could not properly read the configuration file. Backing to default configuration.',file=sys.stderr)
            self._PROJS_FOLD = os.path.expanduser('~/logbuch_projects')
            self._ACT_PROJ = 'default'

        try:
            self._EDITOR = re.findall('EDITOR=\s*(.+)', content)[0]
        except:
            print('Could not properly read the EDITOR in conf file. Using system\'s default.')
            self._EDITOR = os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi'

    def projsDir(self):
        return self._PROJS_FOLD

    def actProj(self):
        return self._ACT_PROJ

    def editor(self):
        return self._EDITOR

    def edit(self):
        # running the text editor
        subprocess.run([self.editor(), self._base+'/'+self._confF])
