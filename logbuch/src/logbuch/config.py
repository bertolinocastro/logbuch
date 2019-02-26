import sys
import subprocess
import os
import re
from whichcraft import which

# TODO: URGENT!!!!!!!!! Convert it to configparser class from python

class Config(object):
    _base = '~/.logbuch'
    _confF = 'conf.cfg'
    _content =  "PROJECTS_FOLDER=%s\n"+\
                "ACTIVE_PROJECT=%s\n"+\
                "EDITOR=%s\n"+\
                "EXTENSION=%s\n"+\
                "PDF_CMD=%s"


    _PROJS_FOLD = ''
    _ACT_PROJ = ''
    _EDITOR = ''
    _EXT = ''
    _PDF_CMD = ''

    def __init__(self):
        self._base = os.path.expanduser(self._base)
        self._confOpen()

    def _confOpen(self):
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
                'topics', 'vi','.md','pdftex %log_file%')
            with open(self._base+'/'+self._confF,'w') as f:
                f.write(content)
        # ---

        try:
            self._PROJS_FOLD = re.findall('PROJECTS_FOLDER\s*=\s*(.+)', content)[0]
            self._ACT_PROJ = re.findall('ACTIVE_PROJECT\s*=\s*(.+)', content)[0]
            self._EXT = re.findall('EXTENSION\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: could not properly read the configuration file. Backing to default configuration.',file=sys.stderr)
            self._PROJS_FOLD = os.path.expanduser('~/logbuch_projects')
            self._ACT_PROJ = 'topics'
            self._EXT = '.md'

        try:
            self._EDITOR = re.findall('EDITOR=\s*(.+)', content)[0]
        except:
            print('Could not properly read the EDITOR in conf file. Using system\'s default.')
            self._EDITOR = os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi'

        try:
            self._PDF_CMD = re.findall('PDF_CMD\s*=\s*(.+)',content)[0]
            if not '%log_file%' in self._PDF_CMD:
                print('PDF_CMD parameter in config file has no %log_file% as input!')
                sys.exit()
            name = self._PDF_CMD.split(' ')[0]
            if not self._hasTool(name):
                print('Your system does not have %s installed. Trying pdftex...')
                if not self._hasTool('pdftex'):
                    print('Could not find a LaTeX compiler on your system. Please, provide one in config file.')
                    sys.exit()
                else:
                    self._PDF_CMD = 'pdftex %log_file%'
        except:
            print('Could not properly read PDF_CMD in config file. Trying to use pdftex.')
            self._PDF_CMD = 'pdftex %log_file%'

    def projsDir(self):
        return self._PROJS_FOLD

    def actProj(self):
        #TODO: insert a way to get the actual project/it's the last one or the one sended to the command line
        return self._ACT_PROJ

    def editor(self):
        return self._EDITOR

    def edit(self):
        # running the text editor
        subprocess.run([self.editor(), self._base+'/'+self._confF])

    def getExt(self):
        return self._EXT

    def setActive(self,proj):
        self._ACT_PROJ = proj
        self._confSave()

    def _confSave(self):
        content = self._content%(self._PROJS_FOLD,self._ACT_PROJ,self._EDITOR,self._EXT)
        with open(self._base+'/'+self._confF,'w') as f:
            f.write(content)

    def _hasTool(self,name):
        return which(name) is not None
