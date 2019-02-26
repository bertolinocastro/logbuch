import os
import shutil
import sys
import click

def prompProj(config,proj):
    path = config.projsDir()
    act = config.actProj()

    # listing topics inside active or all projects
    lis = sorted(listDir(path))

    if proj:
        if proj in lis:
            print('Switching to existing project "%s"\n'%proj)
        else:
            print('Creating new project "%s" and setting as active\n'%proj)
            createProj(path,proj)
            lis = sorted(lis+[proj]) # appending regarding the order
        config.setActive(proj)
        # printing projects tree
        printTree(lis,path,proj,numbers=False)
    else:
        # printing projects tree
        if len(lis)<1:
            print('No Project to list in %s!\nPlease, create one first with an argument to "-p" option.'%path)
            sys.exit()

        printTree(lis,path,act)
        res = promptAns(lis)
        if res == -1:
            sys.exit()
        elif res == -2:
            print('\nEntered delete mode!')
            res = promptAns(lis,remove=True)
            if res == -1:
                sys.exit()
            if click.confirm('\nProject "%s" is going to be deleted. Are you sure?'%lis[res]):
                delProj(path,lis[res])
                print('Deleted.')
                if lis[res] == act:
                    print('Switching to %s\n'%lis[0])
                    config.setActive(lis[0])
                lis.remove(lis[res])
        else:
            print('Switching to %s\n'%lis[res])
            config.setActive(lis[res])

def createProj(path,proj):
    os.mkdir(path+'/'+proj)

def delProj(path,proj):
    shutil.rmtree(path+'/'+proj)

def listDir(path):
    if not os.path.exists(path):
        print('Projects folder absent! %s'%path)
        sys.exit()

    projs = [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]
    return projs

# it prints the entire found project tree
def printTree(lis,path,active,numbers=True):
    basenm = os.path.basename(path)

    left_padd = ' '*(len(basenm)+1)
    print('\n '+basenm+chr(9488)+'\n'+left_padd+chr(9474))

    lth = max([len(x) for x in lis])
    for j,key in enumerate(lis):
        isAct = ' * ' if key == active else ' '*3
        app_num = str(j+1) if numbers else ''

        if len(lis) <= 1:
            left_bar = chr(9492)
        elif j == len(lis) -1: # last row
            left_bar = chr(9492)
        else: # all other rows
            left_bar = chr(9500)
        print(left_padd+left_bar+chr(9472)*8+isAct+'%s'%key+' '*(lth-len(key)+1)+app_num)
    print()

def promptAns(lis,remove=False):
    padd = (' '*(2+len(str(len(lis)))))
    if not remove:
        msg = ' [1~%d]: make project active\n'%len(lis) +\
            ' %s-1: asks a project to delete\n'%padd+\
            ' %s 0: exits gracefully\n'%padd
    else:
        msg = ' [1~%d]: delete project\n'%len(lis)+\
            ' %s 0: exits gracefully\n'%padd
    msg1 = 'Choose a number: '
    opts = list(range(-2,len(lis))) if not remove else list(range(-1,len(lis)))
    res = inputNumber(msg+msg1)-1
    while res not in opts:
        res = inputNumber('\nWrong choice. It must be one of:\n%s\n%s'%(msg,msg1))-1
    return res

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))
    except ValueError:
       print('Option must be a number!')
       continue
    else:
       return userInput
       break
