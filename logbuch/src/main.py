import sys
import click
from .logbuch import Logbuch

@click.command(context_settings=dict(max_content_width=120,help_option_names=['-h', '--help']))
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using PyLaTeX')
@click.option('-l','--list',is_flag=True,metavar='[project]',help='List contents of project passed as SUBJECT. If "all" is passed, list all projects content. If nothing is passed, defaults to list all subjects inside actual project')
@click.option('-rm','--remove',is_flag=True,help='Remove a Subject from active Project')
@click.option('--conf',is_flag=True,help='Open the configuration file [default ~/.logbuch/conf.cfg]')
@click.option('--proj',is_flag=True,help='Prompt to choose the active project')
@click.argument('subject',nargs=-1)
def cli(make,list,remove,conf,proj,subject):
    """Here comes the description message."""
    # TODO: finish the command description above.

    # getting single string subject
    subject = treatInput(subject)
    if checkArgs(make,list,remove,conf,proj,subject):
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    config = Logbuch.Config()

    # TODO: create a git option to add,commit,push to an url saved in the config file

    if conf:
        config.edit()
    elif proj:
        Logbuch.prompProj(config)
    elif make:
        Logbuch.make(config)
    elif list:
        Logbuch.list(config,subject)
    elif remove:
        Logbuch.remove(subject,config)
    else:
        Logbuch.buch(subject,config)

def checkArgs(make,list,remove,conf,proj,subject):
    # print(make,list,remove,conf,subject)
    # print([make,list,remove,conf,proj,(subject!='') and not (list^remove)])
    if sum([make,list,remove,conf,proj,(subject!='') and not (list ^ remove)])>1:
        return True

def treatInput(s):
    return ' '.join(s).lower()
