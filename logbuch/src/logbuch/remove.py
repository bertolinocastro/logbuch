import os
import sys
import click
import re

def remove(file,config):
    if not file:
        print('You must pass an argument to -rm option.')
        sys.exit()

    path = config.projsDir()
    actv = config.actProj()
    ext  = config.getExt()

    file = unheadarise(file)

    files = os.listdir(path+'/'+actv)
    if len(files) <= 0:
        print('Actual project is empty!\nUse -l option to check existing subjects')
        sys.exit(0)

    if os.path.exists(path+'/'+actv+'/'+file+ext):
        print('\nSubject "%s" in project "%s" will be deleted.'%(headarise(file),actv))
        print(fileInfo(path+'/'+actv+'/'+file+ext))
        if click.confirm('Are you sure?',abort=True):
            os.remove(path+'/'+actv+'/'+file+ext)
    else:
        print('This subject doest not exist in "%s" project!\nUse -l option to check existing subjects'%actv)

def fileInfo(file):
    with open(file,'r') as f:
        content = f.read()
        try:
            res  = '\nDate of creation: %s\n'%re.findall('Date: (\d{2}\.\d{2}\.\d{4})',content)[0]
            res += 'Contents: %d lines'%len(re.findall('\n',content))
            res += ' and %d characters\n'%len(content)
        except:
            res = '\nCould not read file contents! You shall see its contents before deleting it.\n'
        return res
    return ''

def unheadarise(s):
    return '_'.join(s.lower().split(' '))

def headarise(s):
    return ' '.join(s.capitalize().split('_'))
