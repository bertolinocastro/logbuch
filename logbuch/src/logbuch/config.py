import sys
import subprocess
import os
import re
from whichcraft import which

# TODO: URGENT!!!!!!!!! Convert it to configparser class from python

class Config(object):
    # args passed
    _buch = None
    _list = None
    _remv = None
    _make = None
    _cfgF = None
    _prmp = None
    _topc = None

    _base = '~/.logbuch'
    _confF = 'conf.cfg'
    _content =  "PROJECTS_FOLDER=%s\n"+\
                "ACTIVE_PROJECT=%s\n"+\
                "EDITOR=%s\n"+\
                "EXTENSION=%s\n"


    _PROJS_FOLD = ''
    _ACT_PROJ = ''
    _EDITOR = ''
    _EXT = ''

    _PDF_CMD = ''
    _PDF_CMD_def = 'latexmk'
    _PDF_CMD_FULL_def = _PDF_CMD_def+' -pdf -silent %log_file%'
    _default_PDF_DIR = '~/.logbuch/tex_tmp'

    def __init__(self,make,list,remove,conf,proj,subject):
        self._get_cmd_args(make,list,remove,conf,proj,subject)

        self._base = os.path.expanduser(self._base)
        self._default_PDF_DIR = os.path.expanduser(self._default_PDF_DIR)
        self._confOpen()

    def _get_cmd_args(self,make,list,remove,conf,proj,subject):
        self._buch = (subject!='') and (make^list^remove^proj)
        self._list = list
        self._remv = remove
        self._make = make
        self._cfgF = conf
        self._prmp = proj

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
                'default', 'vi','.md')
            with open(self._base+'/'+self._confF,'w') as f:
                f.write(content)
        # ---

        try:
            self._PROJS_FOLD = re.findall('PROJECTS_FOLDER\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read PROJS_FOLD in configuration file. Backing to default.')
            self._PROJS_FOLD = os.path.expanduser('~/logbuch_projects')

        try:
            self._ACT_PROJ = re.findall('ACTIVE_PROJECT\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read ACT_PROJ in configuration file. Backing to default.')
            self._ACT_PROJ = 'default'

        try:
            self._EXT = re.findall('EXTENSION\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read EXTENSION in configuration file. Backing to default.')
            self._EXT = '.md'

        try:
            self._EDITOR = re.findall('EDITOR\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read the EDITOR in conf file. Using system\'s default or trying "vi" if none.')
            self._EDITOR = os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi'

        try:
            tmp = re.findall('PDF_CMD\s*=\s*(.+)',content)
            if len(tmp)<1:
                if self._make:
                    raise NoLaTeXTool
                else:
                    raise
            self._PDF_CMD = tmp
            if not '%log_file%' in self._PDF_CMD:
                print('PDF_CMD parameter in config file has no %log_file% as argument!')
                if self._make:
                    raise NoLogFile
            else:
                name = self._PDF_CMD.split(' ')[0]
                if self._make and not self._hasTool(name):
                    print('Your system does not have "%s" installed. Checking %s...'%(name,self._PDF_CMD_def))
                    raise NoLaTeXTool
        except NoLogFile:
            sys.exit()
        except NoLaTeXTool:
            if not self._hasTool(self._PDF_CMD_def):
                print('Could not find %s as LaTeX compiler on your system. Please, provide an existing one in config file.'%self._PDF_CMD_def)
                if self._make:
                    sys.exit()
            else:
                self._PDF_CMD = self._PDF_CMD_FULL_def
        except:
            pass

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

    def getDefTexDir(self):
        return os.path.expanduser(self._default_PDF_DIR)

    def _hasTool(self,name):
        return which(name) is not None

    def pdfCompiler(self):
        v = self._PDF_CMD.split(' ')
        cmd = v[0]
        args = v[1:]
        return [cmd,args]

class NoLogFile(Exception):
    pass

class NoLaTeXTool(Exception):
    pass
