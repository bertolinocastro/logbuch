import sys
import click
from .logbuch import Logbuch

@click.command()
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using PyLaTeX')
@click.option('-l','--list',is_flag=True,help='List all subjects inside this project')
@click.option('-rm','--remove',help='Remove a subject')
@click.option('--conf',is_flag=True,help='Open the configuration file')
@click.argument('subject',default='')
def cli(make,list,remove,conf,subject):
    if sum([make,list,remove!=None,subject!='',conf])>1:
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    config = Logbuch.Config()
    # TODO: create a way to divide the logbuch per project

    if conf:
        config.edit()
    elif make:
        Logbuch.make(config)
    elif list:
        Logbuch.list(config)
    elif remove:
        Logbuch.remove(remove,config)
    else:
        Logbuch.buch(subject,config)
