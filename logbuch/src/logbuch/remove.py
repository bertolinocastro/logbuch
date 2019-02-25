import os
import sys
import click
import re

def remove(file,config):
    # print(file)

    path = config.projsDir()
    actv = config.actProj()
    ext  = config.getExt()

    file = unheadarise(file)

    files = os.listdir(path+'/'+actv)
    if len(files) <= 0:
        print('Actual project is empty!')
        sys.exit(0)

    if os.path.exists(path+'/'+actv+'/'+file+ext):
        print('\nSubject "%s" in project "%s" will be deleted.'%(file,actv))
        print(fileInfo(path+'/'+actv+'/'+file+ext))
        if click.confirm('Are you sure?',abort=True):
            os.remove(path+'/'+actv+'/'+file+ext)
    else:
        print('This file doest not exist!')

def fileInfo(file):
    with open(file,'r') as f:
        content = f.read()
        res  = 'Date of creation: %s\n'%re.findall('Date: (\d{2}\.\d{2}\.\d{4})',content)[0]
        res += 'Contents: %d lines'%len(re.findall('\n',content))
        res += ' and %d characters\n'%len(content)
        return res
    return ''

def unheadarise(s):
    return '_'.join(s.lower().split(' '))
