import os
import sys
import click
import builtins
from .logbuch import Logbuch
from .autocompletion import auto_comp_callback

__version__ = '1.0'

# @click.command(context_settings=dict(max_content_width=120, help_option_names=['-h', '--help'], ignore_unknown_options=True))
@click.command(context_settings=dict(max_content_width=120, help_option_names=['-h', '--help']))
@click.option('-mk', '--make', is_flag=True, help='Compile subjects to a .tex file using defined LaTeX compiler')
@click.option('-l', '--list', is_flag=True, metavar='[project]', help='List contents of project passed as SUBJECT. If "all" is passed, list all projects content. If nothing is passed, defaults to list all subjects inside actual project')
@click.option('-p', '--proj', is_flag=True, help='Prompt to choose the active project. If you pass an argument, it will create and/or activate that.')
@click.option('-rm', '--remove', is_flag=True, help='Remove a Subject from active Project')
@click.option('-g', '--git', is_flag=True, help='Redirect all arguments passed to the git command')
@click.option('-c', '--conf', is_flag=True, help='Open the configuration file [default ~/.logbuch/conf.cfg]')
@click.argument('subject', nargs=-1, type=click.STRING, autocompletion=auto_comp_callback)
def cli(make, list, remove, conf, proj, git, subject):
    """Logbuch\t(version 1.0)

    A less-do-more program to take your notes quickly before you forget them.

    It also compiles in LaTeX for your LabBook/research history. :-)

    """
    config = Logbuch.Config(make, list, remove, conf, proj, git, subject)

    args = builtins.list(subject)
    # getting single string subject
    subject = treatInput(subject,config.getExt())
    if checkArgs(make, list, remove, conf, proj, git, subject):
        print('Sorry, but only one option is accepted')
        sys.exit(1)

    # allowing only git redirection mode to receive '.' as argument beginning
    if not git and checkHidden(subject):
        print('Hidden Projects or Subjects are not allowed! "%s"' % subject)
        sys.exit()


    if conf:
        config.edit()
    elif proj:
        Logbuch.prompProj(config, subject)
    elif make:
        Logbuch.make(config, subject)
    elif list:
        Logbuch.list(config, subject)
    elif remove:
        Logbuch.remove(subject, config)
    elif git:
        Logbuch.git(config, args)
    else:
        Logbuch.buch(subject, config)


def checkArgs(make, list, remove, conf, proj, git, subject):
    if sum([make, list, remove, conf, proj, (subject != '') and not (list ^ remove ^ make ^ proj ^ git)]) > 1:
        return True


def treatInput(s,ext):
    return '_'.join(s).replace(ext,'').lower()


def checkHidden(s):
    return s and '.' == s.strip()[0]
