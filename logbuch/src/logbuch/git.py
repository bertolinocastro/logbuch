import os
import sys
import subprocess
import datetime

class Git:
    def autoCommit(conf, subj,changedC,changedL):
        cwd = conf.projsDir()
        act = conf.actProj()
        now = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')

        # checking repository existence
        if not _has_repository(cwd):
            print('Cannot procede auto commiting. There is no repository at "%s".'%cwd)
            return

        # adding file
        subprocess.run(['git','add',act+'/'+subj],cwd=cwd)

        # commiting addition
        msg = '%+d lines, %+d chars to "%s" at %s'%(changedL,changedC,act+'/'+subj,now)
        subprocess.run(['git','commit','-m',msg],cwd=cwd)

    def wrapper(conf,args):
        cwd = conf.projsDir()

        # checking repository existence
        if not _has_repository(cwd,args):
            print('Cannot procede with redirection. There is no repository at "%s".'%cwd)
            sys.exit()

        subprocess.run(['git']+args,cwd=cwd)

def _has_repository(path,args=[]):
    if 'init' in args and os.path.exists(path): # allowing to create a repository
        return True
    try:
        ret = subprocess.run(['git','status'],cwd=path,capture_output=True)
        return ret.returncode == 0
    except:
        return False
