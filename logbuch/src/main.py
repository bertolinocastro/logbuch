import click
from .logbuch import Logbuch

@click.command()
@click.option('-m','--make',is_flag=True,help='Compile subjects to a .tex file using PyLaTeX')
@click.option('-l','--list',is_flag=True,help='List all subjects inside this project')
@click.option('-rm','--remove',help='Remove a subject')
@click.argument('subject',default='')
def cli(make,list,remove,subject):
    print(make,list,remove,subject)

    click.echo('Hello World!')

    Logbuch.make('tst')
