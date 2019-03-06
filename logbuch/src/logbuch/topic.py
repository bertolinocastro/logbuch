import os
import pathlib
import sys
import datetime
import re
import time
import getpass
import difflib
import readline

from .git import Git

class Topic(object):
    _base = ''
    _subject = None
    _isNew = False
    _ext = ''
    _path = None

    _conf = None

    _full_content = ''

    _file_len = 0
    _file_lines = 0

    def __init__(self,subject,conf,proj=None):
        if proj is None:
            self._base = conf.projsDir()+'/'+conf.actProj()
        else:
            self._base = conf.projsDir()+'/'+proj

        self._ext = conf.getExt()
        self._conf = conf

        self._check_hidden(subject)

        # checking wheter there is the base folder
        if not os.path.exists(conf.projsDir()):
            print('No root projects folder found. Creating %s'%self._base)
        elif not os.path.exists(self._base):
            print('No active project folder found. Creating %s'%self._base)

        pathlib.Path(self._base).mkdir(parents=True, exist_ok=True)

        if subject:
            self._subject = self._file_titable(subject)
            # check if it already exists
            self._isNew = not os.path.exists(self._base+'/'+self._subject+self._ext)
        else:
            files = [x for x in os.listdir(self._base) if '.' != x[0] and self._ext in x]
            if len(files) > 0:
                tstamps = [os.path.getmtime(self._base+'/'+file) for file in files]
                id = tstamps.index(max(tstamps))
                lastf = files[id]
                self._subject = self._file_titable(lastf)
                print('Opening last modified Subject: %s'%self._headarise(self._subject))
                if self._checkBoolInput('Abort? [y/n]: '):
                    sys.exit(0)
            else:
                self._isNew = True
                self._get_subject()

        self._path = self._base +'/'+ self._subject + self._ext
        self._get_contents()

        self._header_h = TopicHeader(self._subject,conf,proj)

    def _check_hidden(self,subj):
        if subj and '.' == subj[0]:
            print('Hidden subjects "%s" are not allowed!'%subj)
            sys.exit()

    def _get_subject(self):
        self._subject = self._file_titable(input('Empty "%s" folder. Please write a subject: '%self._base))

    def _get_contents(self):
        with open(self._path, 'a+') as f:
            f.seek(0)
            self._full_content = f.read()

    def _write_contents(self,f):
        f.write(self._full_content)

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def path(self):
        return self._path

    def close(self):
        newLen, newLine = self._get_file_len()
        changedC = newLen - self._file_len
        changedL = newLine - self._file_lines
        print('\nSubject "%s" saved!\nContent changed: %+d char, %+d lines\n'%(self._headarise(self._subject),changedC,changedL))

        new_cont = self._get_full_content_open()
        for line in difflib.unified_diff(self._full_content.split('\n'),new_cont.split('\n'),'Original','Current',lineterm=''):
            print(line)

        if (changedC or changedL) and self._conf.isAutoCommit():
            print('\nGit autocommiting...\n\n')
            Git.autoCommit(self._conf,self._subject+self._ext,changedC,changedL)

        self._header_h.close()

    def _get_full_content_open(self):
        with open(self._path,'r') as f:
            return f.read()
        return ''

    def _get_file_len(self):
        r = 0
        s = 0
        with open(self._path, 'a+') as f:
            r = f.tell()
            f.seek(0)
            s = sum([1 for line in f])
        return r,s

    def _checkBoolInput(self,str):
        res = input(str)
        return 'y' == res or 'Y' == res

    def _file_titable(self,s):
        return '_'.join(s.lower().split(' ')).replace(self._ext,'')

    def getFileContents(self):
        return {'path':     self.path(),
                'subj':     self._headarise(self._subject),
                'text':     self._full_content,
                'header':   self._header_h.getFileContents()
        }

    def getHeaderContents(self):
        return self._header_h.getFileContents()

# header helper class
class TopicHeader(object):
    _base = ''
    _subject = None
    _isNew = False
    _ext = ''
    _path = None

    _conf = None

    _title = ''
    _author = ''
    _date = ''
    _full_content = ''

    _file_len = 0
    _file_lines = 0

    def __init__(self,subject,conf,proj=None):
        if proj is None:
            self._base = conf.projsDir()+'/'+conf.actProj()
        else:
            self._base = conf.projsDir()+'/'+proj

        self._subject = subject
        self._ext = '.yaml'
        self._conf = conf

        self._isNew = not os.path.exists(self._base+'/.'+self._subject+self._ext)
        self._path = self._base +'/.'+ self._subject + self._ext
        self._get_contents()

    def _get_contents(self):
        with open(self._path, 'a+') as f:
            f.seek(0)
            self._get_full_content(f)
            if not self._isNew:
                overWrite = False
                if self._file_has_content(f):
                    if not self._check_std_header():
                        print('"%s" does not match the standard header.'%self._headarise(self._subject))
                        overWrite = True
                else:
                    print('"%s" does not have the minimum content.'%self._headarise(self._subject))
                    overWrite = True

                if overWrite:
                    if not self._checkBoolInput('Subject header content is going to be prepended by the new header.\nAre you sure? [y/n]: '):
                        sys.exit(0)
                    print('Prepending...')
                    f.truncate(0)

                    self._get_header()
                    self._write_contents(f)
            else:
                self._get_header()
                self._write_contents(f)

    def _check_std_header(self):
        cnt = self._full_content
        hd = re.findall(r'---(.*?)\.\.\.',cnt,re.DOTALL)
        if hd:
            tt = re.findall(r'\s*subj-titl:\s+(.+)',hd[0])
            au = re.findall(r'\s*subj-auth:\s+(.+)',hd[0])
            dt = re.findall(r'\s*subj-date:\s+(.+)',hd[0])
            try:
                if tt: self._title = tt[0]
                if au: self._author = au[0]
                if dt: self._date = dt[0]
                return tt and au and dt
            except:
                return False
        else:
            return False

    def _get_full_content(self,f):
        self._full_content = f.read()
        f.seek(0)

    def _file_has_content(self,file):
        pos0 = file.tell()
        file.seek(0,2)
        pos1 = file.tell()

        self._file_len = pos1

        if pos1 < pos0 + 30:
            return False

        file.seek(pos0)
        self._file_lines = sum([1 for line in file])
        file.seek(pos0)

        if self._file_lines < 5:
            return False
        return True

    def _write_contents(self,f):
        f.write('---\n') # yaml header
        f.write('    subj-titl: %s\n'%self._title) # title
        f.write('    subj-auth: %s\n'%self._author) # authors
        f.write('    subj-date: %s\n'%self._date) # date
        f.write('...\n\n')
        f.write(self._full_content)

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def _get_header(self):
        if not self._title:  self._title  = self._headarise(self._subject)
        if not self._author: self._author = [getpass.getuser()]
        if not self._date:   self._date   = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    def path(self):
        return self._path

    def close(self):
        newLen, newLine = self._get_file_len()
        changedC = newLen - self._file_len
        changedL = newLine - self._file_lines

        if (changedC or changedL):
            print('\nSubject header %s saved!\nContent changed: %+d char, %+d lines\n'%(self._headarise(self._subject),changedC,changedL))

        new_cont = self._get_full_content_open()
        for line in difflib.unified_diff(self._full_content.split('\n'),new_cont.split('\n'),'Original','Current',lineterm=''):
            print(line)

        if (changedC or changedL) and self._conf.isAutoCommit():
            print('\nGit autocommiting...\n\n')
            Git.autoCommit(self._conf,self._subject+self._ext,changedC,changedL)

    def _get_full_content_open(self):
        with open(self._path,'r') as f:
            return f.read()
        return ''

    def _get_file_len(self):
        r = 0
        s = 0
        with open(self._path, 'a+') as f:
            r = f.tell()
            f.seek(0)
            s = sum([1 for line in f])
        return r,s

    def _checkBoolInput(self,str):
        res = input(str)
        return 'y' == res or 'Y' == res

    def _file_titable(self,s):
        return '_'.join(s.lower().split(' ')).replace(self._ext,'')

    def getFileContents(self):
        return {'path':     self.path(),
                'subj':     self._headarise(self._subject),
                'title':    self._title,
                'author':   self._author,
                'date':     self._date,
                'text':     self._full_content
        }
