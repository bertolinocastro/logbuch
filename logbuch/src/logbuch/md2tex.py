import os
import shutil
import sys
import re
import subprocess
import time
import click
import getpass
import pypandoc
from .topic import Topic
from .tplates import Tplates

class Md2Tex(object):
    """A class to hold all static methods to convert a markdown to a latex file content"""

    _tex_header = '\n'.join([
        r'\documentclass[a4paper,12pt]{report}',
        r'\usepackage[utf8x]{inputenc}',
        r'\usepackage[left=3.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm]{geometry}',
        r'\usepackage[bookmarks]{hyperref}',
        r'\usepackage{helvet}',
        r'\renewcommand{\familydefault}{\sfdefault}',
        r'\renewcommand{\thesection}{\arabic{section}} % This removes the "0.x" section indexing'
        ])

    _tex_title = r'\title{\Huge{%s}%s}'
    _tex_author = r'\author{%s}'
    _tex_date = r'\date{%s}'

    _tex_begin = r'\begin{document}'
    _tex_end   = r'\end{document}'

    _tex_mkttle = '\n'+r'\maketitle'
    _tex_tbcntents = '\n'+r'\tableofcontents' + '\n'

    _tex_part = '\n'.join([r'\part*{%s%s}',r'\addcontentsline{toc}{part}{%s}']) + '\n'
    _tex_part_sub = r'\\ \bigskip\bigskip\bigskip\bigskip\bigskip\normalfont\Large{%s}'
    _tex_part_aut = r'\\ \bigskip\bigskip\bigskip\bigskip\bigskip\normalfont\large{%s}'
    _tex_part_dat = r'\\ \bigskip\normalfont\large{%s}'
    _tex_chapter = '\n'.join([r'\chapter*{\LARGE{%s}\\ \normalfont\large{\textit{%s}}}',
        r'\addcontentsline{toc}{chapter}{%s}',r'\setcounter{section}{0}']) + '\n'

    _tex_text = ''

    _config = None
    _proj = None
    _texFile = None

    _projects = None

    _pandoc_header = ''
    _tex_subtitle_h = ''
    _tex_authors_h = []
    _tex_date_h = ''

    _pandoc_args = []

    _tplates = None

    _pandoc_output = ''

    def __init__(self,config,proj):
        self._config = config
        self._proj = proj
        self._tplates = Tplates(config)

        path = config.projsDir() # projects root

        if config.getPandocExArgs() is not None:
            self._pandoc_args = config.getPandocExArgs()

        # listing topics inside active or all projects
        dic = listDir(path,proj,config.getExt())
        self._projects = list(dic)

        self._get_header_file(None)

        self._get_title(config)
        self._get_author(config)
        self._get_contents(dic,config)
        self._writeContents()

    def _get_header_file(self,proj):
        self._clean_std_header()
        if proj:
            path = self._config.projsDir()+'/'+proj+'/.header.md'
        else:
            path = self._config.projsDir()+'/.header.md'
        if os.path.exists(path):
            with open(path,'r') as f:
                self._pandoc_header = f.read()
                self._check_std_header(path)

    def _check_std_header(self,path):

        lines = self._pandoc_header.split('\n')
        if len(lines)>2:
            tt = re.fullmatch(r'%\s(.+)',lines[0])
            au = re.fullmatch(r'%\s(.+)',lines[1])
            dt = re.fullmatch(r'%\s(.+)',lines[2])
            try:
                if tt: self._tex_subtitle_h= tt.groups()[0]
                if au: self._tex_authors_h = au.groups()[0].split(';')
                if dt: self._tex_date_h = dt.groups()[0]
                return tt and au and dt
            except:
                return False
        else:
            print('ERROR: Could not read Pandoc hidden header at "%s".'%path)

    def _clean_std_header(self):
        self._tex_subtitle_h= ''
        self._tex_authors_h = []
        self._tex_date_h = ''

    def _get_title(self,config):
        self._tex_title = self._tex_title%('Logbuch',
            r'\\ \bigskip\bigskip\large{%s}'%self._tex_subtitle_h if self._tex_subtitle_h else r'')
        if self._tex_date_h:
            self._tex_title = self._tex_date%self._tex_date_h + self._tex_title

    def _get_author(self,config):
        self._tex_author = self._tex_author%' \and '.join(self._tex_authors_h) if self._tex_authors_h else self._tex_author%getpass.getuser()

    def _get_contents(self,dic,config):
        logb_tplt = self._tplates.logb_template()
        meta_yaml = self._tplates.meta_yaml()
        proj_tplt = self._tplates.proj_template()
        subj_tplt = self._tplates.subj_template()

        for proj in sorted(dic):
            proj_yaml = self._tplates.proj_yaml(proj)
            self._add_content([
                self._convert_md(None, proj_tplt,proj_yaml)
            ])

            if len(dic[proj]) < 1:
                print('Warning: Project %s is Empty!'%proj)
                continue

            topC = [Topic(topic,config,proj=proj).getFileContents() for topic in dic[proj]]
            date = [_tstamp(cont['header']['date']) for cont in topC]
            ordr = _argsort(date)

            for itopic in ordr:
                cont = topC[itopic]
                top_yaml = self._append_body_yaml(cont['header']['path'],cont['text'])
                self._add_content([
                    self._convert_md(None,subj_tplt,top_yaml,text=True)
                ])

        final_yaml = self._append_body_yaml(meta_yaml,self._tex_text)
        self._pandoc_output = ext = self._convert_md(None,logb_tplt,final_yaml,text=True)

    def _convert_md(self,subj,template,yaml,outfile=None,text=False):
        if text:
            convert = pypandoc.convert_text
        else:
            convert = pypandoc.convert_file
        if subj:
            return convert(subj, 'latex', format='md', outputfile=outfile,
                extra_args=['--template='+template])
        else:
            return convert(yaml, 'latex', format='md', outputfile=outfile,
                extra_args=['--template='+template])

    def _writeContents(self):
        path = self._config.projsDir()
        self._proj = self._proj if self._proj else 'all'
        self._texFile = path+'/'+self._proj+'.tex'

        if not os.path.exists(self._texFile) or click.confirm('Output TeX file %s already exists. Would you like to overwrite?'%self._texFile):
            with open(self._texFile,'w') as f:
                f.write(self._pandoc_output)

    def _append_body_yaml(self,path,text):
        bdy_tplt = '\n'.join([r'---',r'body: |',r'{cnt}',r'...'])
        with open(path,'r') as f:
            cnt = f.read()
            return cnt+bdy_tplt.format(cnt='\n    '.join(['']+text.splitlines()+['']))
        return ''

    def editContents(self):
        if click.confirm('Would you like to edit the tex file?'):
            subprocess.run([self._config.editor(), self._texFile])

    def _add_content(self,s):
        self._tex_text += '\n'.join(s)+'\n'

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def compile(self):
        # print(self._tex_text)

        oldCd = os.getcwd()
        os.chdir(self._config.projsDir())

        cmds = self._config.pdfCompiler()

        for cmdi in cmds:
            cmd = list(cmdi)[0]
            args = cmdi[cmd]
            args = [x.replace('%log_file%',self._texFile) for x in args]

            try:
                ret = subprocess.run([cmd]+args,capture_output=True,check=True)
                if ret.returncode != 0:
                    raise Exception(ret.stdout+'\n'+ret.stderr)
            except Exception as e:
                print('Something went wrong with compilation step. Error message below:\n')
                print(repr(e))
                sys.exit()

        os.chdir(oldCd)

        projs = self._projects
        print('Project%s %s compiled as %s.pdf'%('s' if len(projs)>1 else '',
                       ','.join(projs), self._proj))

# -----

def listDir(path,proj,ext):
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
        projs = [x for x in os.listdir(path) if '.' != x[0] and os.path.isdir(path+'/'+x)]

    for proj in projs:
        if proj not in dic:
            dic[proj] = []
        for topic in os.listdir(path+'/'+proj):
            if not '.' == topic[0] and topic.endswith(ext): # ignoring hidden files
                dic[proj].append(topic)

    return dic

def _ignoreExt(s):
    return s != '.tex' and s != '.swp'

def _argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def _tstamp(s):
    return time.mktime(time.strptime(s, "%d.%m.%Y %H:%M"))
