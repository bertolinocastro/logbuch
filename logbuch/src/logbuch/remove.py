import os
import sys
import click
import re
from .topic import Topic

def remove(file,config):
    if not file:
        print('You must pass an argument to -rm option.')
        sys.exit()

    path = config.projsDir()
    actv = config.actProj()
    ext  = config.getExt()

    # file = unheadarise(file)

    files = os.listdir(path+'/'+actv)
    if len(files) <= 0:
        print('Actual project is empty!\nUse "-l all" option to check other projects contents')
        sys.exit(0)

    if os.path.exists(path+'/'+actv+'/'+unheadarise(file)+ext):
        print('\nSubject "%s" in project "%s" will be deleted.'%(headarise(file),headarise(actv)))
        top = Topic(file,config)
        print(fileInfo(top.getFileContents()))
        if click.confirm('Are you sure?',abort=True):
            top.delete()
    else:
        print('This subject doest not exist in "%s" project!\nUse -l option to check existing subjects'%actv)

def fileInfo(dic):
    res  = '\nDate of creation: %s\n'%dic['header']['date']
    res += 'Contents: %d lines'%len(dic['text'].splitlines())
    res += ' and %d characters\n'%len(dic['text'])
    return res

def unheadarise(s):
    return '_'.join(s.lower().split(' '))

def headarise(s):
    return ' '.join(s.capitalize().split('_'))
