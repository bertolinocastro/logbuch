import os
import sys
import datetime
import re
import time

class Topic(object):
    _base = 'topics'
    _subject = None
    _isNew = False
    _ext = '.md'
    _path = None

    _header = ''
    _date = ''

    _file_len = 0

    def __init__(self,_subject):
        # checking wheter there is the base folder
        if not os.path.exists(self._base):
            os.mkdir(self._base)

        if _subject:
            self._subject = _subject
            # check if it already exists
            self._isNew = not os.path.exists(self._base+'/'+self._subject+self._ext)
        else:
            files = [x for x in os.listdir(self._base) if self._ext in x]
            if len(files) > 0:
                tstamps = [os.path.getmtime(self._base+'/'+file) for file in files]
                id = tstamps.index(max(tstamps))
                lastf = files[id]
                self._subject = lastf.replace(self._ext,'')
                print('Opening last modified file: %s'%self._subject)
                if self._checkBoolInput('Abort? [y/n]: '):
                    sys.exit(0)
            else:
                self._isNew = True
                self._get_subject()

        self._path = self._base +'/'+ self._subject + self._ext
        self._get_contents()

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
        newLen = self._get_file_len()
        changed = newLen - self._file_len
        print('Topic %s saved!\nContent changed: %+d char'%(self._subject,changed))

    def _get_file_len(self):
        r = 0
        with open(self._path, 'a+') as f:
            r = f.tell()
        return r

    def _checkBoolInput(self,str):
        res = input(str)
        return 'y' == res or 'Y' == res
