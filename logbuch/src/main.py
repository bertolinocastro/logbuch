import sys
import click
from .logbuch import Logbuch

@click.command(context_settings=dict(max_content_width=120,help_option_names=['-h', '--help']))
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using PyLaTeX')
@click.option('-l','--list',is_flag=True,metavar='[project]',help='List all subjects inside actual project or all if project name is "all"')
@click.option('-rm','--remove',metavar='<topic>',help='Remove a subject')
@click.option('--conf',is_flag=True,help='Open the configuration file [default ~/.logbuch/conf.cfg]')
@click.argument('subject',default='')
def cli(make,list,remove,conf,subject):
    """Here comes the description message."""
    # TODO: finish the command description above.

    if checkArgs(make,list,remove,conf,subject):
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    config = Logbuch.Config()
    # TODO: create a way to divide the logbuch per project

    if conf:
        config.edit()
    elif make:
        Logbuch.make(config)
    elif list:
        Logbuch.list(config,subject)
    elif remove:
        Logbuch.remove(remove,config)
    else:
        Logbuch.buch(subject,config)

def checkArgs(make,list,remove,conf,subject):
    # print(make,list,remove,conf,subject)
    # print([make,list,remove!=None,conf,(subject!='') and not list])
    if sum([make,list,remove!=None,conf,(subject!='') and not list])>1:
        return True
