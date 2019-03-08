import os
import sys

def list(conf,proj):
    path = conf.projsDir() # projects root
    actu = conf.actProj()  # actual active project
    proj = proj if proj else actu # if a project name was passed
    extt = conf.getExt()
    ignore = conf.ignoreDirs()

    # listing topics inside active or all projects
    dic = listDir(path,proj,extt,ignore)
    printTree(dic,conf.getExt(),actu,path)

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

# it prints the entire found project tree
def printTree(dic,ext,active,path):
    basenm = os.path.basename(path)

    left_padd = ' '*(len(basenm)+1)
    print('\n '+basenm+chr(9488)+'\n'+left_padd+chr(9474))

    # 9116 -> barra vertical -> 9474
    # |- -> 9500
    # 9472 -> barra horizontal
    # 9492 -> '>'
    # 9516 -> -.-
    # 9488 -> >.
    if len(dic) < 1:
        dic['No Projects to list!'] = ['']

    lth = max([len(x) for x in dic])
    for j,key in enumerate(sorted(dic)):
        isAct = ' * ' if key == active else ' '*3
        if len(dic[key]) < 1:
            dic[key].append('Empty project!')

        for i,top in enumerate(sorted(dic[key])):
            top = _headarise(top.replace(ext,''))
            if i == 0: # first row
                left_bar = chr(9500) if j < len(dic)-1 else chr(9492)
                right_symb = ' '+chr(9516) if len(dic[key]) > 1 else ' '
                print(left_padd+left_bar+chr(9472)*8+isAct+'%s'%_headarise(key)+right_symb+chr(9472)*5+' %s'%top)
            elif i == len(dic[key])-1 and len(dic[key]) > 1: # last row
                left_bar = chr(9474) if j < len(dic)-1 else ' '
                print(left_padd+left_bar+' '*(12+len(key))+chr(9492)+chr(9472)*5+' %s'%top)
            else: # middle rows
                left_bar = chr(9474) if j < len(dic)-1 else ' '
                print(left_padd+left_bar+' '*(12+len(key))+chr(9500)+chr(9472)*5+' %s'%top)
    print()

def _file_titable(s,ext):
    return '_'.join(s.lower().split(' ')).replace(ext,'')
def _headarise(s):
    return ' '.join(s.capitalize().split('_'))
