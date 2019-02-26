import os
import shutil
import sys
from .topic import Topic
import subprocess
import click
import getpass

class Md2Tex(object):
    """A class to hold all static methods to convert a markdown to a latex file content"""

    _tex_header = '\n'.join([
        r'\documentclass[12pt]{article}',
        r'\usepackage[utf8x]{inputenc}',
        r'\usepackage[left=3.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm]{geometry}',
        r'\usepackage{helvet}',
        r'\renewcommand{\familydefault}{\sfdefault}'
        ])

    _tex_title = r'\title{%s}'
    _tex_author = r'\author{%s}'

    _tex_begin = r'\begin{document}'
    _tex_end   = r'\end{document}'

    _tex_mkttle = '\n'+r'\maketitle'
    _tex_tbcntents = '\n'+r'\tableofcontents'

    _tex_section    = '\n''\n'.join([r'\newpage',r'\section{%s}'])
    _tex_subsection = r'\subsection[%s \qquad \small{\textit{%s}}]{%s\\ \normalfont{\small{%s}}}'

    _tex_text = ''

    _config = None
    _proj = None
    _texFile = None

    _projects = None

    def __init__(self,config,proj):
        self._config = config
        self._proj = proj

        path = config.projsDir() # projects root

        # listing topics inside active or all projects
        dic = listDir(path,proj)
        self._projects = list(dic)

        self._get_title(config)
        self._get_author(config)
        self._get_contents(dic,config)

    def _get_title(self,config):
        self._tex_title = self._tex_title%'Logbuch'

    def _get_author(self,config):
        self._tex_author = self._tex_author%getpass.getuser()

    def _get_contents(self,dic,config):
        self._add_content([self._tex_header,self._tex_title,self._tex_author,self._tex_begin,self._tex_mkttle,self._tex_tbcntents])
        for proj in dic:
            self._add_content([self._tex_section%self._headarise(proj)])

            if len(dic[proj]) < 1:
                print('Warning: Project %s is Empty!'%proj)
                self._add_content([
                    self._convert_md(None)
                ])

            for topic in dic[proj]:
                top = Topic(topic,config)
                cont = top.getFileContents()
                self._add_content([
                    self._tex_subsection%(cont['header'],cont['date'],cont['header'],cont['date']),
                    self._convert_md(cont['text'])
                ])

        self._add_content([self._tex_end])

    # TODO: call convert md 2 latex procedures
    def _convert_md(self,s):
        if s:
            return s
        else:
            return r'\textit{Nothing here!}'+'\n'

    def writeContents(self):
        path = self._config.projsDir()
        self._proj = self._proj if self._proj else 'all'
        self._texFile = path+'/'+self._proj+'.tex'

        if not os.path.exists(self._texFile) or click.confirm('Output TeX file %s already existis. Would you like to overwrite?'%self._texFile):
            with open(self._texFile,'w+') as f:
                f.write(self._tex_text)

    def editContents(self):
        if click.confirm('Would you like to edit the tex file?'):
            subprocess.run([self._config.editor(), self._texFile])

    def _add_content(self,s):
        self._tex_text += '\n'.join(s)+'\n'

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def compile(self):
        oldCd = os.getcwd()
        os.chdir(self._config.projsDir())

        cmd,args = self._config.pdfCompiler()
        args = [x.replace('%log_file%',self._texFile) for x in args]
        ret = subprocess.run([cmd]+args,capture_output=True,check=True)
        if ret.returncode != 0:
            print('Something went wrong with compilation step. Error message below:')
            print(ret.stdout)
            sys.exit()

        args = ['-c','-silent'] # cleaning step
        ret = subprocess.run([cmd]+args,capture_output=True,check=True)
        if ret.returncode != 0:
            print('Something went wrong with compilation step. Error message below:')
            print(ret.stdout)
            sys.exit()

        os.chdir(oldCd)

        projs = self._projects
        print('Project%s %s compiled as %s.tex'%('s' if len(projs)>1 else '',
                ','.join(projs), self._proj))

# -----

def listDir(path,proj):
    if not os.path.exists(path):
        print('Projects folder absent! %s'%path)
        sys.exit()
    if not os.path.exists(path+'/'+proj):
        print('Project folder absent! %s'%path+'/'+proj)
        sys.exit()

    dic = {}
    if proj:
        projs = [proj]
    else:
        projs = [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

    for proj in projs:
        if proj not in dic:
            dic[proj] = []
        for topic in os.listdir(path+'/'+proj):
            if not '.' == topic[0]: # ignoring hidden files
                dic[proj].append(topic)

    return dic

def _ignoreExt(s):
    return s != '.tex' and s != '.swp'
