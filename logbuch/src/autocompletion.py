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

    def check(a, b, c): return a in c or b in c

    if check('-mk', '--make', args) or check('-p', '--proj', args):
        projs = [x for x in listProj(root) if x.startswith(incomplete)]
        ret = projs if len(args) < 2 else []
    elif check('-l', '--list', args):
        projs = [x for x in listProj(root) + ['all'] if x.startswith(incomplete)]
        ret = projs if len(args) < 2 else []
    elif check('-g', '--git', args):
        ret = _get_git_completion(root, actP, args, incomplete)
    elif check('-c', '--conf', args) or check('-h', '--help', args):
        ret = []
    else:  # with no options passed or with -rm/--remove
        files = [x.replace(exte, '') for x in listFiles(root, actP)
                 [actP] if exte in x and incomplete in x]
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
