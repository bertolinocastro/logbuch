import os

def prompProj(config):
    path = config.projsDir()
    act = config.actProj()

    # listing topics inside active or all projects
    lis = sorted(listDir(path))
    printTree(lis,path,act)

    res = promptAns(lis)
    print('Switching to %s\n'%lis[res])
    config.setActive(lis[res])

def listDir(path):
    if not os.path.exists(path):
        print('Projects folder absent! %s'%path)
        sys.exit()

    projs = os.listdir(path)
    return projs

# it prints the entire found project tree
def printTree(lis,path,active):
    basenm = os.path.basename(path)

    left_padd = ' '*(len(basenm)+1)
    print('\n '+basenm+chr(9488)+'\n'+left_padd+chr(9474))

    lth = max([len(x) for x in lis])
    for j,key in enumerate(lis):
        isAct = ' * ' if key == active else ' '*3

        if len(lis) <= 1:
            left_bar = chr(9472)
        elif j == len(lis) -1: # last row
            left_bar = chr(9492)
        else: # all other rows
            left_bar = chr(9500)
        print(left_padd+left_bar+chr(9472)*8+isAct+'%s'%key+' '*(lth-len(key)+1)+str(j+1))
    print()

def promptAns(lis):
    msg = 'Choose a project number to activate: '
    res = inputNumber(msg)-1
    while res not in list(range(len(lis))):
        res = inputNumber('Wrong choice. It must be between %d and %d\n'%(1, len(lis))+msg)-1
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
