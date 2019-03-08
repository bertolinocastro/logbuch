import sys
import subprocess
import os
import re
from whichcraft import which
from configparser import ConfigParser

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

    _confF_absent = False

    _base = '~/.logbuch'
    _confF = 'conf.cfg'
    _path = ''

    _cfg_default = None
    _cfg_dict = None

    _PROJS_FOLD = ''
    _ACT_PROJ = ''
    _EDITOR = ''
    _EXT = ''

    _PDF_CMD = None
    _PDF_CMD_def = 'latexmk'
    _PDF_CMD_FULL_def  = _PDF_CMD_def+' -pdf -silent logbuch_file'
    _PDF_CMD_CLEAR_def = _PDF_CMD_def+' -c -silent'
    _default_PDF_DIR = '~/.logbuch/tex_tmp'

    _G_AUTO_COMMIT = None
    _PANDOC_EXTRA_ARGS = None

    _cfg_parser = None

    def __init__(self,make,list,remove,conf,proj,git,subject):
        self._get_cmd_args(make,list,remove,conf,proj,git,subject)

        self._base = os.path.expanduser(self._base)
        self._path = self._base+'/'+self._confF
        self._default_PDF_DIR = os.path.expanduser(self._default_PDF_DIR)
        self._set_default_config()
        self._confOpen()

    def _set_default_config(self):
        self._cfg_default = dict(
            projects_folder=os.path.expanduser('~/logbuch_projects'),
            active_project='default',
            editor=os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vi',
            extension='.md',
            pdf_cmd=','.join([self._PDF_CMD_FULL_def,self._PDF_CMD_CLEAR_def]),
            g_auto_commit=True,
            pandoc_from_format='markdown',
            pandoc_to_format='latex',
            pandoc_extra_args=','.join(['--biblatex','--listings'])
        )

    def _get_cmd_args(self,make,list,remove,conf,proj,git,subject):
        self._buch = (subject!='') and (make^list^remove^proj^git)
        self._list = list
        self._remv = remove
        self._make = make
        self._cfgF = conf
        self._prmp = proj
        self._gitt = git

    def _fake_section_header(self):
        try:
            with open(self._path, 'r') as f:
                cnt = f.read()
                return u'[USER]\n'+cnt if not '[USER]' in cnt else cnt
        except:
            self._confF_absent = True
            return u'[USER]\n'

    def _add_logbuch_section(self):
        config = self._cfg_parser
        dat = config.items('USER',raw=True)
        if not config.has_section('USER'):
            config.add_section('USER')
        for item in dat:
            config.set('USER',item[0],item[1])

    def _confOpen(self):
        config = ConfigParser(self._cfg_default)
        config.read_string(self._fake_section_header())
        dat = dict(config.items('USER',raw=True))
        self._cfg_parser = config
        self._cfg_dict = dat

        self._add_logbuch_section()

        self._PDF_CMD = self._check_pdf_tool(dat['pdf_cmd'])
        self._PANDOC_EXTRA_ARGS = self._check_pandoc_ex_args(dat['pandoc_extra_args'])

        if self._confF_absent:
            self._confSave()

    def _check_pdf_tool(self,tool):
        try:
            tmp = tool.split(',')
            if not any('logbuch_file' in x for x in tmp):
                raise Exception('PDF_CMD parameter in config file does not have logbuch_file as argument for any command!')
            for cmd in tmp:
                tool = cmd.split(' ')[0]
                if not self._hasTool(tool):
                    raise Exception('Your system does not have "%s" installed.'%tool)
            return tmp
        except Exception as e:
            print(repr(e))
            if self._make: sys.exit()
            return ['']

    def _check_pandoc_ex_args(self,s):
        return s.split(',')

    def confDir(self):
        return self._base

    def projsDir(self):
        return self._cfg_parser.get('USER','projects_folder')

    def actProj(self):
        return self._cfg_parser.get('USER','active_project')

    def editor(self):
        return self._cfg_parser.get('USER','editor')

    def edit(self):
        # running the text editor
        subprocess.run([self.editor(), self._path])

    def getExt(self):
        return self._cfg_parser.get('USER','extension')

    def getFromToFormats(self):
        return self._cfg_parser.get('USER','pandoc_from_format'),\
            self._cfg_parser.get('USER','pandoc_to_format')

    def setActive(self,proj):
        self._cfg_parser.set('USER','active_project',proj)
        self._confSave()

    def _confSave(self):
        try:
            with open(self._path,'w') as f:
                self._cfg_parser.write(f)
        except:
            print('Could not save configuration to "%s".\nWriting it out to stdout and exiting.'%self._path)
            self._cfg_parser.write(sys.stdout)
            sys.exit()

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
        return self._cfg_parser.getboolean('USER','g_auto_commit')

    def getPandocExArgs(self):
        return self._PANDOC_EXTRA_ARGS
