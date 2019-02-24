import os
import sys

def list(conf,proj):

    # print('\n\n\n')

    path = conf.projsDir() # projects root
    actu = conf.actProj()  # actual active project
    proj = proj if proj else actu # if a project name was passed

    # print(path,actu,'<'+proj+'>','\n\n')

    # listing topics inside active or all projects
    dic = listDir(path,proj)
    printTree(dic,conf.getExt(),actu)

def listDir(path,proj):
    if not os.path.exists(path):
        print('Projects folder absent! %s'%path)
        sys.exit()

    dic = {}
    if proj != 'all':
        projs = [proj]
    else:
        projs = os.listdir(path)

    for proj in projs:
        if proj not in dic:
            dic[proj] = []
        for topic in os.listdir(path+'/'+proj):
            dic[proj].append(topic)
        if len(dic[proj]) <= 0:
            del dic[proj]

    return dic

def printTree(dic,ext,active):
    # it prints the entire found project tree
    print(dic,'\n\n')
    print('Listing:\n|')

    lth = max([len(x) for x in dic])
    for j,key in enumerate(sorted(dic)):
        isAct = ' * ' if key == active else '---'
        left_bar = '|' if j < len(dic)-1 else ' '
        for i,top in enumerate(sorted(dic[key])):
            top = ' '.join(top.replace(ext,'').capitalize().split('_')) # getting it as _headarise does
            if i == 0: # first row
                left_bar = '|' if j < len(dic)-1 else '>'
                right_symb = '-.-' if len(dic[key]) > 1 else '---'
                print(left_bar+'-'*8+isAct+'%s'%key+right_symb+'-'*10+' %s'%top)
            elif i == len(dic[key])-1 and len(dic[key]) > 1: # last row
                left_bar = '|' if j < len(dic)-1 else ' '
                print(left_bar+' '*(12+len(key))+'-'+'-'*11+' %s'%top)
            else: # middle rows
                left_bar = '|' if j < len(dic)-1 else ' '
                print(left_bar+' '*(12+len(key))+'+'+'-'*11+' %s'%top)
    print()
