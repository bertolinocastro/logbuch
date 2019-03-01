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
    _gitt = None
    _topc = None

    _base = '~/.logbuch'
    _confF = 'conf.cfg'
    _content =  "PROJECTS_FOLDER=%s\n"+\
                "ACTIVE_PROJECT=%s\n"+\
                "EDITOR=%s\n"+\
                "EXTENSION=%s\n"+\
                "PDF_CMD=%s\n"+\
                "G_AUTO_COMMIT=%s\n"

    _PROJS_FOLD = ''
    _ACT_PROJ = ''
    _EDITOR = ''
    _EXT = ''

    _PDF_CMD = None
    _PDF_CMD_def = 'latexmk'
    _PDF_CMD_FULL_def  = _PDF_CMD_def+' -pdf -silent %log_file%'
    _PDF_CMD_CLEAR_def = _PDF_CMD_def+' -c -silent'
    _default_PDF_DIR = '~/.logbuch/tex_tmp'

    _G_AUTO_COMMIT = None

    def __init__(self,make,list,remove,conf,proj,git,subject):
        self._get_cmd_args(make,list,remove,conf,proj,git,subject)

        self._base = os.path.expanduser(self._base)
        self._default_PDF_DIR = os.path.expanduser(self._default_PDF_DIR)
        self._confOpen()

    def _get_cmd_args(self,make,list,remove,conf,proj,git,subject):
        self._buch = (subject!='') and (make^list^remove^proj)
        self._list = list
        self._remv = remove
        self._make = make
        self._cfgF = conf
        self._prmp = proj
        self._gitt = git

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
                'default', 'vi','.md',self._PDF_CMD_FULL_def,'YES')
            with open(self._base+'/'+self._confF,'w') as f:
                f.write(content)
        # ---

        # PROJECTS_FOLDER
        try:
            self._PROJS_FOLD = re.findall('PROJECTS_FOLDER\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read PROJS_FOLD in configuration file. Backing to default.')
            self._PROJS_FOLD = os.path.expanduser('~/logbuch_projects')

        # ACTIVE_PROJECT
        try:
            self._ACT_PROJ = re.findall('ACTIVE_PROJECT\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read ACT_PROJ in configuration file. Backing to default.')
            self._ACT_PROJ = 'default'

        # EXTENSION
        try:
            self._EXT = re.findall('EXTENSION\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read EXTENSION in configuration file. Backing to default.')
            self._EXT = '.md'

        # EDITOR
        try:
            self._EDITOR = re.findall('EDITOR\s*=\s*(.+)', content)[0]
        except:
            print('ERROR: Could not properly read the EDITOR in conf file. Using system\'s default or trying "vi" if none.')
            self._EDITOR = os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi'

        # PDF_CMD
        try:
            tmp = re.findall('PDF_CMD\s*=\s*(.+)',content)
            if len(tmp)<1:
                raise NoLaTeXTool
            self._PDF_CMD = [x.strip() for x in tmp[0].split(';')]
            if not any('%log_file%' in x for x in self._PDF_CMD):
                print('PDF_CMD parameter in config file has no %log_file% as argument for any command!')
                if self._make:
                    raise NoLogFile
            else:
                for cmd in self._PDF_CMD:
                    name = cmd.split(' ')[0]
                    if self._make and not self._hasTool(name):
                        print('Your system does not have "%s" installed. Try default commands for safety reasons.'%(name))
                        raise NoLaTeXTool
        except NoLogFile:
            sys.exit()
        except NoLaTeXTool:
            if not self._hasTool(self._PDF_CMD_def):
                print('Could not find %s as LaTeX compiler on your system. Please, provide an existing one in config file.'%self._PDF_CMD_def)
                if self._make:
                    sys.exit()
            else:
                self._PDF_CMD = [self._PDF_CMD_FULL_def,self._PDF_CMD_CLEAR_def]
        except Exception as e:
            print('ERROR: Unexpected error ocurred while triying to read PDF_CMD parameter in config file...\n%s'%repr(e))

        # G_AUTO_COMMIT
        try:
            if 'G_AUTO_COMMIT' in content:
                tmp = re.findall('G_AUTO_COMMIT\s*=\s*(.+)', content)[0]
                self._G_AUTO_COMMIT = True if tmp == 'YES' else False
            else:
                self._G_AUTO_COMMIT = True
        except:
            print('ERROR: Could not properly read the G_AUTO_COMMIT in conf file. Using default flag "YES"')
            self._G_AUTO_COMMIT = True

    def projsDir(self):
        return self._PROJS_FOLD

    def actProj(self):
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
        print(self._PDF_CMD)
        content = self._content%(self._PROJS_FOLD,self._ACT_PROJ,self._EDITOR,self._EXT,
            ';'.join(self._PDF_CMD),self._G_AUTO_COMMIT)
        with open(self._base+'/'+self._confF,'w') as f:
            f.write(content)

    def getDefTexDir(self):
        return os.path.expanduser(self._default_PDF_DIR)

    def _hasTool(self,name):
        return which(name) is not None

    def pdfCompiler(self):
        cmd = []
        for c in self._PDF_CMD:
            cc = c.split(' ')
            cmd.append({cc[0]:cc[1:]})
        return cmd

    def isAutoCommit(self):
        return self._G_AUTO_COMMIT

class NoLogFile(Exception):
    pass

class NoLaTeXTool(Exception):
    pass
