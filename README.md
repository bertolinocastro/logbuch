<img src="https://bertolinocastro.github.io/logbuch/logo.png" align="right" title="Logbuch logo">

# Logbuch

A less-do-more program to take your notes quickly before you forget them.

It also compiles in LaTeX for your LabBook/research history. :-)

## Description

Logbuch is a command line tool aimed to quickly take notes while you're closer to a terminal.

Logbuch works handling _Markdown_ files. Each of these files is treated as a _Subject_ and is where the notes are taken. Logbuch groups many _Subjects_ inside its _Project_, as defined by the user.

Each _Subject_ content is converted from _Markdown_ to _LaTeX_ syntax and then becomes a _subsection_ inside its _Project_ _section_. It can also handle figures from one's work/analysis.

## Motivation

As I am pursuing the scientific career, I have noticed that small, but no less important, information are lost quickly while doing day-by-day tasks. Such information can be the separation point between doing unnecessary rework and starting a new day at the next step.

So, I saw that writing concise information, that one can remember without struggling the mind to know what that is supposed to mean, is a huge time improvement. For instance: remote meetings tasks, deliberations and agreements; internet how-to's; papers sentences that one used as reference for one's work or procedures; detailed notes of one's work issues and methodology; thoughts and impressions that one consider important to remember later on; etc.

Besides, I felt that writing them as fast as one can just open one's text editor at any working directory is the point to not forget them.

## Table of Contents

## Features

- [x] Creation, edition, save, deletion and listing of _Subjects_
- [x] Creation, deletion and listing of _Projects_
- [x] Creation, edition and compilation to _LaTeX_
- [ ] Conversion of _Markdown_ tags to _LaTeX_ ones
- [ ] Integration with git
- [ ] _What more? Feel free to ask desired features._

## Installation

Logbuch is written with _setuptools_, as it's aimed to be easy to install.

**Warning:** Logbuch was only tested at Linux environments (Ubuntu specifically), so if any issues occur on your installation, please let me know.

### Requirements

Logbuch depends on:
1. [Python 3.7](https://www.python.org/downloads/release/python-370/) or newer
2. [Pip3](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
3. [Click](https://click.palletsprojects.com/en/7.x/)
4. [Whichcraft](https://github.com/pydanny/whichcraft)
5. [Python3 venv](https://docs.python.org/3/library/venv.html)
6. Any text editor callable from terminal <sup>1</sup>
7. Any _LaTeX_ compiler callable from terminal <sup>2</sup>

<sup>1</sup> Commonly used are: vi, vim, nano, emacs.  
<sup>2</sup> I would strongly suggest `latexmk` for this purpose, since it was the best in my tests.

### Automated install

To install Logbuch in a virtual environment, i.e., that works like a _container_, use `demo_install.sh` as follows:

```sh
$ source ./demo_install.sh
```

Or, if your `python3` command in `PATH` does not correspond to version 3.7 or higher:

```sh
$ PYTHON=<python command> source ./demo_install.sh

# for instance:
$ PYTHON=python3.7 source ./demo_install.sh
# or
$ PYTHON=/usr/bin/python3.7 source ./demo_install.sh
```

To install Logbuch system-wide, follow the same steps before using `install.sh` as follows:

```sh
$ ./install.sh
# or
$ PYTHON=<python command> ./install.sh
```

### Manual install

After installing all dependencies:

```sh
$ git clone https://github.com/bertolinocastro/logbuch.git
$ cd logbuch
$ python3 -m pip install .
```

_**Warning**_ _One may get the last command not to work even after installing `python3.7` or higher. In order to solve that, just `export` prepending your newer python command to `PATH`. You may also create an alias for it or create a symlink. There are many resources on the web to solve this problem._

## Configuration

After installing Logbuch, it will use its default configuration. This file is stored at `~/.logbuch/conf.cfg` You can change it at any time using the `-c` option.

The default configuration file is as follows:

```sh
PROJECTS_FOLDER=/home/user/logbuch_projects
ACTIVE_PROJECT=default
EDITOR=vi
EXTENSION=.md
PDF_CMD=latexmk -pdf -silent %log_file%
```

In parts:

1. PROJECTS_FOLDER=/home/user/logbuch_projects
  It's the full path to where all projects will be stored as well as the compiled _LaTeX_ output. I would suggest it to be a git repository, as you will probably care about the history of your notes.
2. ACTIVE_PROJECT=default
  It's the name of the active _Project_ that Logbuch uses to create new _Subjects_. You should not care about this parameter, just don't let it empty, so it will use the entire _default_ as actual _Project_ name.
3. EDITOR=vi
  It's the command which Logbuch calls when you use any edition option. The command just needs to accept a file name as argument. This is not a problem, since the majority of command line text editors follows this rule.
4. EXTENSION=.md
  It's the extension used on all _Subject_ text files. Logbuch does not discriminate which one is used. Just be advised that it saves and reads using the **same** extension, so do not change it without refactoring your old files extension.
5. PDF_CMD=latexmk -pdf -silent %log_file%
  It's the full command used to compile your _Subjects_ in a _LaTeX_ document. You can pass any arguments to your _LaTeX_ compiler. Just make sure that your command is the first space-ended string after the **=** and that it has `%log_file%`, as this is where the input **.tex** file will the replaced.

## Usage

## Credits



(falar sobre o labbook de bia?)

## License

© Bertolino

Licensed under the [MIT License](LICENSE.txt)
