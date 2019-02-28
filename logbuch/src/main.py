import sys
import click
from .logbuch import Logbuch

__version__ = '1.0'

@click.command(context_settings=dict(max_content_width=120,help_option_names=['-h', '--help']))
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using defined LaTeX compiler')
@click.option('-l','--list',is_flag=True,metavar='[project]',help='List contents of project passed as SUBJECT. If "all" is passed, list all projects content. If nothing is passed, defaults to list all subjects inside actual project')
@click.option('-rm','--remove',is_flag=True,help='Remove a Subject from active Project')
@click.option('-c','--conf',is_flag=True,help='Open the configuration file [default ~/.logbuch/conf.cfg]')
@click.option('-p','--proj',is_flag=True,help='Prompt to choose the active project. If you pass an argument, it will create and/or activate that.')
@click.argument('subject',nargs=-1)
def cli(make,list,remove,conf,proj,subject):
    """Logbuch\t(version 1.0)

    A less-do-more program to take your notes quickly before you forget them.

    It also compiles in LaTeX for your LabBook/research history. :-)

    """

    # getting single string subject
    subject = treatInput(subject)
    if checkArgs(make,list,remove,conf,proj,subject):
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    config = Logbuch.Config(make,list,remove,conf,proj,subject)

    # TODO: create a git option to add,commit,push to an url saved in the config file

    if conf:
        config.edit()
    elif proj:
        Logbuch.prompProj(config,subject)
    elif make:
        Logbuch.make(config,subject)
    elif list:
        Logbuch.list(config,subject)
    elif remove:
        Logbuch.remove(subject,config)
    else:
        Logbuch.buch(subject,config)

def checkArgs(make,list,remove,conf,proj,subject):
    if sum([make,list,remove,conf,proj,(subject!='') and not (list ^ remove ^ make ^ proj)])>1:
        return True

def treatInput(s):
    return ' '.join(s).lower()
