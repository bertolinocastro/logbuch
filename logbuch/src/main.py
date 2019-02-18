import sys
import click
from .logbuch import Logbuch

@click.command()
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using PyLaTeX')
@click.option('-l','--list',is_flag=True,help='List all subjects inside this project')
@click.option('-rm','--remove',help='Remove a subject')
@click.argument('subject',default='')
def cli(make,list,remove,subject):
    if sum([make,list,remove!=None,subject!=''])>1:
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    # TODO: create a config file that holds, besides all, the directory where the data is stored
    # checkConfig()

    if make:
        Logbuch.make()
    elif list:
        Logbuch.list()
    elif remove:
        Logbuch.remove(remove)
    else:
        Logbuch.buch(subject)
