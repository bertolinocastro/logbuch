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

    _tex_text = ''

    _config = None
    _proj = None
    _texFile = None

    _projects = None

    _pandoc_args = []

    _tplates = None

    _pandoc_output = ''

    def __init__(self,config,proj):
        proj = proj if proj else config.actProj() # if a project name was passed

        self._config = config
        self._proj = proj
        self._tplates = Tplates(config)

        path = config.projsDir() # projects root

        if config.getPandocExArgs() is not None:
            self._pandoc_args = config.getPandocExArgs()

        # listing topics inside active or all projects
        dic = listDir(path,proj,config.getExt(),config.ignoreDirs())
        self._projects = list(dic)
        if len(dic)<1:
            print('No projects to compile!\nMaybe you are passing an ignored directory.')
            sys.exit()

        self._get_contents(dic,config)
        self._writeContents()

    # TODO: Use pyyaml https://pyyaml.org/wiki/PyYAMLDocumentation
    # ..... to create a big YAML block appended to .meta.yaml that
    # ..... will be passed to pandoc as metadata input.
    # ..... Also allowing to use a single template once for compiling.
    # ..... Using YAML arrays and dict-like syntax and using pandoc's
    # ..... $if()$, $for()$ and $var.subvar.subsubvar$ syntax to
    # ..... allow the user to customise in one single file everything.
    # ..... But .subj.yaml and .proj.yaml may stay as is.
    def _get_contents(self,dic,config):
        frm, to = config.getFromToFormats()
        logb_tplt = self._tplates.logb_template()
        meta_yaml = self._tplates.meta_yaml()
        proj_tplt = self._tplates.proj_template()
        subj_tplt = self._tplates.subj_template()

        for proj in sorted(dic):
            proj_yaml = self._tplates.proj_yaml(proj)
            self._add_content([
                self._convert_md(proj_tplt,proj_yaml,frm=frm,to=to)
            ])

            if len(dic[proj]) < 1:
                print('Warning: Project %s is Empty!'%self._headarise(proj))
                continue

            topC = [Topic(topic,config,proj=proj).getFileContents() for topic in dic[proj]]
            date = [_tstamp(cont['header']['date']) for cont in topC]
            ordr = _argsort(date)

            for itopic in ordr:
                cont = topC[itopic]
                top_yaml = self._append_body_yaml(cont['header']['path'],cont['text'])
                self._add_content([
                    self._convert_md(subj_tplt,top_yaml,text=True,frm=frm,to=to,args=self._pandoc_args)
                ])

        # final_yaml = self._append_body_yaml(meta_yaml,self._tex_text)
        final_yaml = self._append_body_yaml(meta_yaml,'Thisisalogbuchdummyvariabletoconvertbody')
        self._pandoc_output = self._convert_md(logb_tplt,final_yaml,text=True,frm=frm,to=to)
        self._pandoc_output = self._pandoc_output.\
            replace('Thisisalogbuchdummyvariabletoconvertbody',self._tex_text)

    def _convert_md(self,template,yaml,outfile=None,text=False,frm='md',to='latex',args=[]):
        if text:
            convert = pypandoc.convert_text
        else:
            convert = pypandoc.convert_file
        return convert(yaml, to, format=frm, outputfile=outfile,
            extra_args=['--template='+template]+args)

    def _writeContents(self):
        path = self._config.projsDir()
        self._proj = self._proj if self._proj else 'all'
        self._texFile = path+'/'+self._proj+'.tex'

        if not os.path.exists(self._texFile) or click.confirm('Output TeX file %s already exists. Would you like to overwrite?'%self._texFile):
            with open(self._texFile,'w') as f:
                f.write(self._pandoc_output)

    def _append_body_yaml(self,path,text):
        with open(path,'r') as f:
            cnt = f.read()
            return cnt+'\n'+text
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
            args = [x.replace('logbuch_file',self._texFile) for x in args]

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
        print('Project%s "%s" compiled as %s.pdf'%('s' if len(projs)>1 else '',
                       ','.join([self._headarise(x) for x in projs]), self._proj))

# -----

def listDir(path,proj,ext,ignore):
    if not os.path.exists(path):
        print('Projects folder absent! %s'%path)
        sys.exit()

    dic = {}
    if proj != 'all':
        if proj[0] == '.':
            print('Hidden project name "%s" is not allowed. It will not be read.'%proj)
            sys.exit()
        if not os.path.exists(path+'/'+proj):
            print('Project folder absent! %s\nPass an existing project as argument. Alternatively, check your active project with "-c" or select one with "-p" options.'%(path+'/'+proj))
            sys.exit()
        projs = [proj] if proj not in ignore else []
    else:
        projs = [x for x in os.listdir(path) if '.' != x[0] and x not in ignore and os.path.isdir(path+'/'+x)]

    for proj in projs:
        if proj not in dic:
            dic[proj] = []
        for topic in os.listdir(path+'/'+proj):
            if not '.' == topic[0] and topic.endswith(ext): # ignoring hidden files
                dic[proj].append(topic)

    return dic

def _argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def _tstamp(s):
    return time.mktime(time.strptime(s, "%d.%m.%Y %H:%M"))
