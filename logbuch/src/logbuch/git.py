import subprocess
import datetime

class Git:
    def autoCommit(conf, subj,changedC,changedL):
        cwd = conf.projsDir()
        act = conf.actProj()
        now = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')

        # adding file
        subprocess.run(['git','add',act+'/'+subj],cwd=cwd)

        # commiting addition
        msg = '%+d lines, %+d chars to "%s" at %s'%(changedL,changedC,act+'/'+subj,now)
        subprocess.run(['git','commit','-m',msg],cwd=cwd)

    def wrapper(conf,args):
        cwd = conf.projsDir()
        subprocess.run(['git']+args,cwd=cwd)
