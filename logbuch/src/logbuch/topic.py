import os
import pathlib
import sys
import datetime
import re
import time

from .git import Git

class Topic(object):
    _base = ''
    _subject = None
    _isNew = False
    _ext = ''
    _path = None

    _conf = None

    _header = ''
    _date = ''
    _text = []

    _file_len = 0
    _file_lines = 0

    def __init__(self,subject,conf):
        self._base = conf.projsDir()+'/'+conf.actProj()
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
        self._subject = input('Empty %s folder. Please write a subject: '%self._base)

    def _get_contents(self):
        with open(self._path, 'a+') as f:
            f.seek(0)
            if not self._isNew:
                overWrite = False
                if self._file_has_content(f):
                    subj = f.readline().strip()
                    date = f.readline().strip()

                    if not 'Subject: ' in subj or self._headarise(self._subject) != subj[9:] or \
                        not 'Date: ' in date or not self._check_date(date[6:]):
                        print('File does not match the standard header.')
                        overWrite = True
                    else:
                        self._header = subj
                        self._date = date
                else:
                    print('File does not have the minimum content.')
                    overWrite = True

                if overWrite:
                    if not self._checkBoolInput('Topic content is going to be overwritten.\nAre you sure? [y/n]: '):
                        sys.exit(0)
                    print('Ovewriting...')
                    f.truncate(0)

                    self._get_header()
                    self._get_date()
                    self._write_contents(f)
            else:
                self._get_header()
                self._get_date()
                self._write_contents(f)

    def _file_has_content(self,file):
        pos0 = file.tell()
        file.seek(0,2)
        pos1 = file.tell()

        self._file_len = pos1

        if pos1 < pos0 + 17:
            return False

        file.seek(pos0)
        s = sum([1 for line in file])
        file.seek(pos0)

        self._file_lines = s

        if s < 2:
            return False
        return True

    def _write_contents(self,f):
        f.write('Subject: %s\n'%self._header)
        f.write('Date: %s\n'%self._date)
        f.write('\n# -------\n')

    def _headarise(self,s):
        return ' '.join(s.capitalize().split('_'))

    def _check_date(self,s):
        pattern = re.compile('^\d{2}\.\d{2}\.\d{4}$')
        return bool(pattern.match(s))

    def _get_header(self):
        self._header = self._headarise(self._subject)

    def _get_date(self):
        now = datetime.datetime.now()
        self._date = now.strftime("%d.%m.%Y")

    def path(self):
        return self._path

    def close(self):
        newLen, newLine = self._get_file_len()
        changedC = newLen - self._file_len
        changedL = newLine - self._file_lines
        print('Topic %s saved!\nContent changed: %+d char, %+d lines'%(self._headarise(self._subject),changedC,changedL))

        if (changedC or changedL) and self._conf.isAutoCommit():
            print('\nGit autocommiting...\n\n')
            Git.autoCommit(self._conf,self._subject+self._ext,changedC,changedL)

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
        return '_'.join(s.split(' ')).replace(self._ext,'')

    def getFileContents(self):
        with open(self._path, 'r') as f:
            content = f.readlines()[4:] # skipping header and dotted line
            self._text = ''.join(content)
        return {'header':   self._headarise(self._subject),
                'date':     self._date[-10:],
                'text':     self._text
        }
