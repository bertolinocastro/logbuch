<img src="https://bertolinocastro.github.io/logbuch/logo.png" align="right" title="Logbuch logo">

![version](https://img.shields.io/badge/version-v1.0-orange.svg)
![platform](http://img.shields.io/badge/platform-linux-brightgreen.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

# Logbuch

A less-do-more program to take your notes quickly before you forget them.

It also compiles in LaTeX for your Lab-Book/research history. :-)

## Description

Logbuch is a command line tool aimed to quickly take notes while you're closer to a terminal.

Logbuch works handling _Markdown_ files. Each of these files is treated as a ___Subject___ and is where the notes are taken. Logbuch groups many _Subjects_ inside its ___Project___, as defined by the user.

Each ___Subject___ content is converted from _Markdown_ to _LaTeX_ syntax and then becomes a _subsection_ inside its ___Project___ _section_. It can also handle figures from one's work/analysis.

## Table of Contents

- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Automated install](#automated_install)
  - [Manual install](#manual_install)
- [Configuration](#configuration)
- [Usage](#usage)
  - [-h](#-h)
- [Supported Markdown tags](#supported_markdown_tags)
- [Issues and desired features](#issues_and_desired_features)
- [Credits](#credits)
- [License](#license)

## Motivation

As I am pursuing the scientific career, I have noticed that small, but no less important, information are lost quickly while doing day-by-day tasks. Such information can be the separation point between doing unnecessary rework and starting a new day at the next step.

So, I saw that writing concise information, that one can remember without struggling the mind to know what that is supposed to mean, is a huge time improvement. For instance: remote meetings tasks, deliberations and agreements; internet how-to's; papers sentences that one used as reference for one's work or procedures; detailed notes of one's work issues and methodology; thoughts and impressions that one consider important to remember later on; etc.

Besides, I felt that writing them as fast as one can just open one's text editor at any working directory is the point to not forget them.

## Features

- [x] Creation, edition, save, deletion and listing of ___Subjects___
- [x] Creation, deletion and listing of ___Projects___
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

<sup>1</sup> Commonly used are: vi, vim, nano, emacs, gedit.  
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

_**Warning**_ _You may notice the last command may not work even after installing `python3.7` or higher. In order to solve that, just `export` prepending your newer python command to `PATH`. You may also create an alias or a symlink for it. There are many resources on the web to solve this problem._

## Configuration

After installing Logbuch, it will use its default configuration, that is stored at `~/.logbuch/conf.cfg`. You can edit it at any time using the `-c` option.

The default configuration file is as follows:

```sh
PROJECTS_FOLDER=/home/user/logbuch_projects
ACTIVE_PROJECT=default
EDITOR=vi
EXTENSION=.md
PDF_CMD=latexmk -pdf -silent %log_file%
```

In parts:

1. `PROJECTS_FOLDER=/home/user/logbuch_projects`  
  It's the full path to where all projects will be stored as well as the compiled _LaTeX_ output. I would suggest it to be a git repository, as you will probably care about the history of your notes.

2. `ACTIVE_PROJECT=default`  
  It's the name of the active ___Project___ that Logbuch uses to create new ___Subjects___. You should not care about this parameter, just don't let it empty, although Logbuch will use _default_ as actual ___Project___ name.

3. `EDITOR=vi`  
  It's the command which Logbuch calls when you use any edition option. The command just needs to accept a file name as argument. This is not a problem, since the majority of command line text editors follows this rule.

4. `EXTENSION=.md`  
  It's the extension used on all ___Subject___ text files. Logbuch does not discriminate which one is used. Just be advised that it saves and reads using the __same__ extension, so do not change it without refactoring your old files extension.

5. `PDF_CMD=latexmk -pdf -silent %log_file%`  
  It's the full command used to compile your ___Subjects___ in a _LaTeX_ document. You can pass any arguments to your _LaTeX_ compiler. Just make sure that your command is the first space-ended string after the __=__ and that it has `%log_file%`, as this is where the input __.tex__ file will the replaced.

FYI:
- Each entry may have spaces before and after the __=__ sign.
- `PDF_CMD` may have a sequence of commands separated by `;`. (~~not yet implemented~~)

## Usage

The basic usage of Logbuch is creating/opening a ___Subject___ inside the active ___Project___. In order to do that you must type:
```sh
logbuch subject name with how many words you want
```
this command will open your text editor with a predefined header. The header contains The ___Subject___ and the date of creation. You must write everything below the `# ------` line, because that information is handled by Logbuch.

If you want to open your last edited ___Subject___ inside the active ___Project___, just type Logbuch without any argument:
```sh
logbuch
```
---
###### `-rm/--remove` option

This option is used to delete any ___Subject___ inside the active ___Project___. It requires an argument that must be the ___Subject___ name. It will prompt your confirmation to delete.
```sh
logbuch -rm subject name with how many words you want
```

---
###### `-p/--proj` option

This option will list your ___Projects___ and give you a number of options to set one ___Project___ as active or delete it with its contents. The `*` sign represents which ___Project___ is active now.
```sh
logbuch -p
```

If you pass an argument to this option, Logbuch will create an ___Project___ if it does not exist and set it as active. _Be aware that this must be one of your first steps while setting Logbuch up for the first time._
```sh
logbuch -p name of your project
```

---
###### `-l/--list` option

This option lists the content of your active ___Project___  if no argument is passed.
```sh
logbuch -l
```

As arguments, it accepts the name of any single ___Project___ you have in your ___Projects___ folder and prints its content or accepts the string "all" and prints the contents of all ___Projects___. As in `-p`, `*` sign represents which ___Project___ is active now.
```sh
logbuch -l name of your project
logbuch -l all
```

---
###### `-m/--make` option

This option will get all content below the `# ------` string inside your ___Subjects___ and put them as `\subsection{}` content in the compiled file.
The ___Subject___ and the date of creation will become the subsection title and subtitle, respectively. Your ___Project___ will become a `\section{}` and its name will be the section title. The author of the compiled _LaTeX_ file is obtained from your system's user name.

Using this option without arguments makes it compile for all ___Projects___ and save the _LaTeX_ output as `all.tex`.
```sh
logbuch -m
```
You may also pass a ___Project___ name, so Logbuch will compile just it with its contents.
```sh
logbuch -m name of your project
```

All outputs are saved in your ___Projects___ folder root and are name with your ___Project___ name followed by `.tex` extension for the _LaTeX_ inputs and `.pdf` for the outputs. Feel free to edit them as you wish.

If you have an existing `.tex` file, Logbuch will prompt you if you want to overwrite it, so you can just recompile a previous `.tex` version.

---
###### `-g/--git` option (~~not implemented~~)

---
###### `-c/--conf` option

This option opens the configuration file `~/.logbuch/conf.cfg` in your text editor, so you can edit it by hand. The parameters were deeply discussed at [Configuration section](#configuration).

---
###### `-h/--help` option
Finally, you can always use the `-h/--help` option to get information about Logbuch options.

---

FYI:
- ___Subject___ and ___Project___ names are allowed to have space. Their leading char will always be capitalized and the remaining lowered. Underscores will be converted to spaces.
-
- Logbuch may handle cases that are not discussed in this README. If you get any trouble using Logbuch, please, let me know.

## Supported Markdown tags (~~not yet implemented~~)
---

## Issues and desired features

(please use the repository Issues page to report any issues and ask desired features)

## Credits

- @bertolinocastro  
    Just the author of Logbuch.

- @waltercostamb  
    Mentor and author of a brilliant workshop showing all purposes of doing Lab-Book at the Academy and her structured and logic way to deal with her research annotations. For more in-deep information, check her [Lab-Book repository](https://github.com/waltercostamb/Lab-Book).

## License

© Bertolino

Licensed under the [MIT License](LICENSE.txt)
