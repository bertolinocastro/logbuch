import os
import pathlib
import sys
import datetime
import re
import time
import getpass
import difflib

from .git import Git

class Topic(object):
    _base = ''
    _subject = None
    _isNew = False
    _ext = ''
    _path = None

    _conf = None

    _title = ''
    _author = ''
    _date = ''
    _text = ''
    _full_content = ''

    _file_len = 0
    _file_lines = 0
    _tripdash_delim_pos = 0

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

    def _check_hidden(self,subj):
        if subj and '.' == subj[0]:
            print('Hidden subjects "%s" are not allowed!'%subj)
            sys.exit()

    def _get_subject(self):
        self._subject = self._file_titable(input('Empty "%s" folder. Please write a subject: '%self._base))
        self._title = self._headarise(self._subject)

    def _get_contents(self):
        with open(self._path, 'a+') as f:
            f.seek(0)
            self._get_full_content(f)
            if not self._isNew:
                overWrite = False
                if self._file_has_content(f):
                    titl = f.readline().strip()
                    auth = f.readline().strip()
                    date = f.readline().strip()
                    f.seek(0)
                    self._text = ''.join(f.readlines()[self._tripdash_delim_pos:])

                    if not self._check_std_header(titl,auth,date):
                        print('"%s" does not match the standard header.'%self._headarise(self._subject))
                        overWrite = True
                else:
                    print('"%s" does not have the minimum content.'%self._headarise(self._subject))
                    overWrite = True

                if overWrite:
                    if not self._checkBoolInput('Topic content is going to be prepended by the header.\nAre you sure? [y/n]: '):
                        sys.exit(0)
                    print('Prepending...')
                    f.truncate(0)

                    self._get_header()
                    self._write_contents(f)
            else:
                self._get_header()
                self._write_contents(f)

    def _check_std_header(self,title,authors,date):
        tt = re.fullmatch(r'%\s(.+)',title)
        au = re.fullmatch(r'%\s(.+)',authors)
        dt = re.fullmatch(r'%\s(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})',date)
        try:
            if tt: self._title = tt.groups()[0]
            if au: self._author = au.groups()[0].split(';')
            if dt: self._date = dt.groups()[0]
            return tt and au and dt
        except:
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
        s = sum([1 for line in file])
        self._file_lines = s

        file.seek(pos0)
        hasDash = False
        for i,line in enumerate(file.readlines()):
            if '---\n' == line:
                hasDash = True
                break
            if i >= 5:
                break
        self._tripdash_delim_pos = i+1 if hasDash else 3
        file.seek(pos0)

        if s < 3:
            return False
        return True

    def _write_contents(self,f):
        f.write('%% %s\n'%self._title) # title
        f.write('%% %s\n'%';'.join(self._author)) # authors
        f.write('%% %s\n'%self._date) # date
        f.write('\n---\n\n')
        f.write(self._full_content)

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def _check_date(self,s):
        pattern = re.compile('^\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}$')
        return bool(pattern.match(s))

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
        print('Topic %s saved!\nContent changed: %+d char, %+d lines\n'%(self._headarise(self._subject),changedC,changedL))

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
        return {'subj':     self._headarise(self._subject),
                'title':    self._title,
                'author':   self._author,
                'date':     self._date,
                'text':     self._text
        }
