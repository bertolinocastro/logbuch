import os
import sys

def list(conf,proj):
    path = conf.projsDir() # projects root
    actu = conf.actProj()  # actual active project
    proj = proj if proj else actu # if a project name was passed

    # listing topics inside active or all projects
    dic = listDir(path,proj)
    printTree(dic,conf.getExt(),actu,path)

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

    lth = max([len(x) for x in dic])
    for j,key in enumerate(sorted(dic)):
        isAct = ' * ' if key == active else ' '*3
        for i,top in enumerate(sorted(dic[key])):
            top = ' '.join(top.replace(ext,'').capitalize().split('_')) # getting it as _headarise does
            if i == 0: # first row
                left_bar = chr(9500) if j < len(dic)-1 else chr(9492)
                right_symb = ' '+chr(9516) if len(dic[key]) > 1 else ' '
                print(left_padd+left_bar+chr(9472)*8+isAct+'%s'%key+right_symb+chr(9472)*5+' %s'%top)
            elif i == len(dic[key])-1 and len(dic[key]) > 1: # last row
                left_bar = chr(9474) if j < len(dic)-1 else ' '
                print(left_padd+left_bar+' '*(12+len(key))+chr(9492)+chr(9472)*5+' %s'%top)
            else: # middle rows
                left_bar = chr(9474) if j < len(dic)-1 else ' '
                print(left_padd+left_bar+' '*(12+len(key))+chr(9500)+chr(9472)*5+' %s'%top)
    print()
