import os
import sys
from .topic import Topic

class Md2Tex(object):
    """A class to hold all static methods to convert a markdown to a latex file content"""

    _tex_header = '\n'.join([
        r'\documentclass[12pt]{article}',
        r'\usepackage[utf8x]{inputenc}',
        r'\usepackage[left=3.5cm, right=1.5cm, top=2.5cm, bottom=2.5cm]{geometry}'
        ])

    _tex_title = r'\title{%s}'
    _tex_author = r'\author{%s}'

    _tex_begin = r'\begin{document}'
    _tex_end   = r'\end{document}'

    _tex_mkttle = r'\maketitle'
    _tex_tbcntents = r'\tableofcontents'

    _tex_section    = r'\section{%s}'
    _tex_subsection = r'\subsection{%s}'

    _tex_text = ''

    def __init__(self,config,proj):
        path = config.projsDir() # projects root

        # listing topics inside active or all projects
        dic = listDir(path,proj)
        print(dic)

        self._get_author(config)
        self._get_contents(dic,config)

    def _get_author(self,config):
        pass

    def _get_contents(self,dic,config):
        self._add_content([self._tex_header,self._tex_title,self._tex_author,self._tex_begin,self._tex_mkttle,self._tex_tbcntents])
        for proj in dic:
            print(proj)
            print(dic[proj])

            self._add_content([self._tex_section%self._headarise(proj)])

            for topic in dic[proj]:
                top = Topic(topic,config)
                cont = top.getFileContents()
                print(cont)
                self._add_content([
                    self._tex_subsection%cont['header'],
                    self._convert_md(cont['text'])
                ])

        self._add_content([self._tex_end])
        print(self._tex_text)

    # TODO: call convert md 2 latex procedures
    def _convert_md(self,s):
        if s:
            return s
        else:
            return r'\textit{Nothing here!}'+'\n'

    # TODO: write the file contents to the destination file
    def writeContents(self):
        pass

    # TODO: open the editor to edit the object file contents
    def editContents(self):
        pass

    def _add_content(self,s):
        print(s)
        self._tex_text += '\n'.join(s)+'\n'

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

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
        projs = os.listdir(path)

    for proj in projs:
        if proj not in dic:
            dic[proj] = []
        for topic in os.listdir(path+'/'+proj):
            if not '.' == topic[0]: # ignoring hidden files
                dic[proj].append(topic)

    return dic
