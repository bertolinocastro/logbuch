import os
import re
import subprocess
from .logbuch import Logbuch
from .logbuch.projpromp import listDir as listProj
from .logbuch.list import listDir as listFiles


def auto_comp_callback(ctx, args, incomplete):
    config = Logbuch.Config(False, False, False, False, False, False, '')
    root = config.projsDir()
    actP = config.actProj()
    exte = config.getExt()
    ignore = config.ignoreDirs()

    def check(a, b, c): return a in c or b in c

    if check('-p', '--proj', args) or check('-mk', '--make', args) or check('-l', '--list', args):
        projs = ['all' if 'all'.startswith(incomplete) else None] \
            if not check('-p','--proj',args) and len(args)<2 else [None]
        _args_remove_option(args)
        l,incomplete = _fancy_incomplete(args,incomplete)
        projs += [_headarise(x)[l+1:] for x in listProj(root,ignore) if _headarise(x).startswith(incomplete)]
        ret = projs
    elif check('-g', '--git', args):
        ret = _get_git_completion(root, actP, args, incomplete)
    elif check('-c', '--conf', args) or check('-h', '--help', args):
        ret = []
    else:  # with no options passed or with -rm/--remove
        _args_remove_option(args,options=['-rm','--remove'])
        l,incomplete = _fancy_incomplete(args,incomplete)
        files = [_headarise(x.replace(exte, ''))[l+1:] for x in listFiles(root, actP,exte,ignore)[actP] \
            if exte in x and _headarise(x).startswith(incomplete)]
        ret = sorted(list(set(files)-set(args)))

    return ret

# This function may only work properly when Click's developpers
# prevent their bashcompletion caller from completing arguments
# as after double dash as if they were the program options yet
def _get_git_completion(root, actP, args, incomplete):
    git_root = '/usr/lib/git-core/'
    args = [x for x in args if x != '--' and x != '-g' and x != '--git']  # removing -- and -g

    if not os.path.exists(git_root):
        return []

    # getting commands
    if len(args) < 1:  # if no git option has been passed yet
        li = [x.replace('git-', '') for x in os.listdir(git_root)
              if os.path.isfile(git_root+x) and x.replace('git-', '').startswith(incomplete)]
        return sorted(li)

    out = subprocess.run(['git']+args+['-h'], capture_output=True)  # .stdout.decode('utf-8')
    out = out.stderr if out.stderr else out.stdout
    out = out.decode('utf-8')

    # tested only with commit yet
    matches = [x for x in re.findall(
        '[\s|\t](-[^\s|,|/|\)|\[]+)', out) if x.startswith(incomplete)]

    doubDash = set([x for x in matches if x.startswith('--')])
    singDash = set(matches) - doubDash

    return list(sorted(singDash)+sorted(doubDash))

def _file_titable(s,ext):
    return '_'.join(s.lower().split(' ')).replace(ext,'')
def _headarise(s):
    return ' '.join(s.capitalize().split('_'))

def _fancy_incomplete(args,incomplete):
    args = ' '.join(args); l = len(args)
    if l>0: incomplete = ' '.join([args,incomplete])
    else: l -=1
    return l,incomplete

def _args_remove_option(args,options=None):
    if not options:
        _options = ['-p','--proj','-g','--git','-mk','--make','-l','--list','-rm','--remove','-c','--conf']
    else: _options = options
    args[:] = [x for x in args if not x in _options]
