from .git import Git

def git(conf,args):
    msgArgs = ' '.join(args)
    print('Redirecting {0} to git as follows:\n\n\tgit {0}\n\n----------\n'.format(msgArgs))
    Git.wrapper(conf,args)
