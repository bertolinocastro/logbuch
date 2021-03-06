<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/logo.png" align="right" title="Logbuch logo">

![version](https://img.shields.io/badge/version-v1.0-orange.svg)
![platform](http://img.shields.io/badge/platform-linux-brightgreen.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

# Logbuch

A less-do-more program to take your notes quickly before you forget them.

It also compiles in LaTeX for your [Lab-Book](https://github.com/waltercostamb/Lab-Book)/research history. :-)

## Basic usage
<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/basic-usage.gif" title="Basic usage">  

## Git integration
<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/git-usage.gif" title="Git integration">  

## _LaTeX_ compilation
<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/make-usage.gif" title="LaTeX compilation">  

## Configuring on first use
<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/first-usage.gif" title="Configuring at first use">  

## Example output
<img src="https://bertolinocastro.github.io/other_repo_webcontent/logbuch/output.tex.gif" align="center" title="Example output">  

_You can see this example and others with Logbuch generated data in this [repository](https://github.com/bertolinocastro/logbuch-example-output)._

## Description

Logbuch is a command line tool aimed to quickly take notes while you're closer to a terminal.

Logbuch works handling any markup input format files (such as _Markdown_, _HTML_, etc). Each of these files is treated as a ___Subject___ and is where the notes are taken. Logbuch groups many ___Subjects___ inside their ___Projects___, as defined by the user.

Each ___Subject___ content is converted from its input format to the output format defined by the user and then becomes a content as defined by the user inside its ___Project___.

_<sup>def</sup>_: By default, Logbuch will convert from [`pandoc`'s _Markdown_](https://pandoc.org/MANUAL.html#pandocs-markdown) to _LaTeX_. However, it's possible to set `input` and `output` formats for `pandoc` conversion.

## Table of Contents

- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Automated install](#automated-install)
  - [Manual install](#manual-install)
- [Configuration](#configuration)
- [Usage](#usage)  
  - [-rm/--remove](#-rm--remove-option)
  - [-p/--proj](#-p--proj-option)
  - [-l/--list](#-l--list-option)
  - [-mk/--make](#-mk--make-option)
  - [-g/--git](#-g--git-option)
  - [-c/--conf](#-c--conf-option)
  - [-h/--help](#-h--help-option)
- [Pandoc conversion](#pandoc-conversion)
    - [___Subject___ conversion](#subject-conversion)
    - [___Project___ conversion](#project-conversion)
    - [Whole document conversion](#whole-document-conversion)
- [Issues and desired features](#issues-and-desired-features)
- [Credits](#credits)
- [License](#license)

## Motivation

As I am pursuing the scientific career, I have noticed that small, but no less important, information are lost quickly while doing daily tasks. Such information can be the separation point between doing unnecessary rework and starting a new day at the next step.

So, I saw that writing concise information, that one can remember without struggling the mind to know what that is supposed to mean, is a huge time improvement. For instance: remote meetings tasks, deliberations and agreements; internet how-to's; papers sentences that one used as reference for one's work or procedures; detailed notes of one's work issues and methodology; thoughts and impressions that one consider important to remember later on; etc.

Besides, I felt that writing them as fast as one can just open one's text editor at any working directory is the point to not forget them.

## Features

- [x] Creation, edition, save, deletion and listing of ___Subjects___
- [x] Creation, deletion and listing of ___Projects___
- [x] Creation, edition and compilation to _LaTeX_
- [x] Integration with git
- [x] Bash completion
- [x] Conversion from _Markdown_ to _LaTeX_
- [ ] _Want more? Feel free to ask desired features as stated [here](#issues-and-desired-features)._

## Installation

Logbuch is written with _setuptools_, as it's aimed to be easy to install.

**Warning:** Logbuch was only tested at Linux environments (Ubuntu specifically), so if any issues occur on your installation, please let me know.

__Warning 2:__ Logbuch will append an `eval` command to your user's shell starter script in order to activate `autocompletion`. At this moment, just `.bashrc` is supported. After installing, it will work on your next login.

### Requirements

Logbuch depends on:
1. [Python 3.7](https://www.python.org/downloads/release/python-370/) or newer
2. [Pip3](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
3. [Click](https://click.palletsprojects.com/en/7.x/)
4. [Whichcraft](https://github.com/pydanny/whichcraft)
5. [pypandoc](https://github.com/bebraw/pypandoc)
6. [Python3 venv](https://docs.python.org/3/library/venv.html)
7. [Pandoc](https://pandoc.org/installing.html) <sup>\*</sup>
8. Any text editor callable from terminal <sup>1</sup>
9. Any _LaTeX_ compiler callable from terminal <sup>2</sup>
10. _LaTeX_ dependencies <sup>!</sup>

Make sure you have installed requirements `1,2,7,8,9` before proceeding to next installation steps. Else requirements should be handled by `setuptools` itself.

<sup>1</sup> Commonly used are: vi, vim, nano, emacs, gedit.  
<sup>2</sup> I would strongly suggest `latexmk` for this purpose, since it was the best in my tests.  
<sup>\*</sup> _Latest version recommended._ I recommend downloading from the GitHub's release, as the `apt` package is not yet updated (at the time of writing this README).  
<sup>!</sup> If you are converting to _LaTeX_, you will probably face problems with dependencies at the compilation step. For the default `templates`, I strongly recommend you to install the following packages: `biber` (for bibliography usage), `texlive-latex-extras`, `texlive-fonts-recommended`, `texlive-fonts-extra`, `texlive-bibtex-extra` and `texlive-base`.

### Automated install

Beforehand, you must get your files:
```sh
$ git clone https://github.com/bertolinocastro/logbuch.git
$ cd logbuch
```

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
---
To install Logbuch system-wide, use `install.sh` script as follows:

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

_**Warning:**_ _You may notice the last command may not work even after installing `python3.7` or higher. In order to solve that, just `export` prepending your newer python command to `PATH`. You may also create an alias or a symlink for it. There are many resources on the web to solve this problem._

## Configuration

After installing Logbuch, it will use its default configuration, that is stored at `~/.logbuch/conf.cfg`. You can edit it at any time using the `-c` option.

The default configuration file is as follows:

```ini
[DEFAULT]
projects_folder = /home/user/logbuch_projects
active_project = default
editor = vi
extension = .md
pdf_cmd = latexmk -pdf -silent logbuch_file, latexmk -c -silent
g_auto_commit = True
ignore_dir =
pandoc_from_format = markdown
pandoc_to_format = latex
pandoc_extra_args = --biblatex,--listings
```

In parts:

1. `projects_folder`  
  It's the full path to where all ___Projects___ will be stored as well as the compiled _LaTeX_ output. I strongly suggest it to be a git repository, as you will probably care about the history of your notes.

2. `active_project`  
  It's the name of the active ___Project___ that Logbuch uses to create new ___Subjects___. You should not care about this parameter, just don't let it empty because Logbuch will emit an error message and you should select or create one through `-p` option.

3. `editor`  
  It's the command which Logbuch calls when you use any edition option. The command just needs to accept a file name as argument. This is not a problem, since the majority of command line text editors follows this rule.

4. `extension`  
  It's the extension used on all ___Subject___ text files. Logbuch does not discriminate which one is used. Just be advised that it saves and reads using the __same__ extension, so do not change it without refactoring your old files extension.

5. `pdf_cmd`  
  It's the full command used to compile your ___Subjects___ in a _LaTeX_ document. You can pass any arguments to your _LaTeX_ compiler. Just make sure that your command is the first space-ended string after the __=__ and that it has `logbuch_file`, as this is where the input __.tex__ file will the replaced. You may also separate multiple commands with `commas`. For instance, the default command will compile to _LaTeX_ and then clean the unnecessary files in output directory.

6. `g_auto_commit`  
  It's a flag. If it results in `True`<sup>1</sup>, Logbuch will do a `git add` and `git commit` every time you change a ___Subject___, else it will do nothing. This is an optional config entry. Default is `True`.

7. `ignore_dir`  
  This field accepts a `comma` separated sequence of directories inside you ___Projects___ folder that Logbuch must ignore at any step. Be aware that hidden directories (that starts with `.`) are already ignored by Logbuch.

8. `pandoc_from_format`  
  It's the input format to be sent to `pandoc`'s `--from` option. Default is `markdown`.

9. `pandoc_to_format`  
  It's the output format to be sent to `pandoc`'s `--to` option. Default is `latex`.

10. `pandoc_extra_args`  
  It's a sequence of `comma` separated arguments and options to be sent to the last `pandoc` call (the final compilation step).

FYI:
- You can make one-line comments with `#` and `;`.
- Each entry may have spaces before and after the `=` sign. For more rules, please read the [Python's ConfigParser documentation](https://docs.python.org/3/library/configparser.html).

<sup>1</sup> This field may handle many inputs and result as `True` or `False`. Please take a look at [Python's ConfigParser doc](https://docs.python.org/3/library/configparser.html#supported-datatypes).

## Usage

The basic usage of Logbuch is creating/opening a ___Subject___ inside the active ___Project___. In order to do that you must type:
```sh
logbuch subject name with how many words you want
```
This command will open your text editor with that ___Subject___ content. It will create an empty file if it's a new one. A predefined header is also created in `YAML` format in a file with the same name but starting with `.` (so it's hidden from standard file managers) in the same folder as the ___Subject___ content file. More details in [this section](#pandoc-conversion).

If you want to open your last edited ___Subject___ inside the active ___Project___, just type Logbuch without any argument:
```sh
logbuch
```

If you want to access a ___Project___ or a ___Subject___ that starts with a `-` or want to safely pass arguments to the `-g/--git` [interface option](#-g--git-option), you must pass `--` right after your first option. For instance:
```sh
logbuch -- --subject -starting--- with -dashes
logbuch -l -- -project --starting-- -with- dashes
logbuch -g -- commit -m "A safely passed commit"
```

As stated in [config](#configuration) parameter `G_AUTO_COMMIT`, every time you change any ___Subject___ file, if Logbuch is in `auto commit mode`, it will try to `add` and `commit` that ___Subject___. In order to work, Logbuch expects that there is a `git` repository inside your ___Projects___ root folder.

---
###### `-rm/--remove` option

This option is used to delete any ___Subject___ and its header inside the active ___Project___. It requires an argument that must be the ___Subject___ name. It will prompt your confirmation to delete.
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

With arguments, it accepts the name of any single ___Project___ you have in your ___Projects___ folder and prints its ___Subjects___. It may also accept the string `all` and print the contents of all ___Projects___. As in `-p`, `*` sign represents which ___Project___ is active now.
```sh
logbuch -l name of your project
logbuch -l all
```

---
###### `-mk/--make` option

Using this option without arguments makes it compile the active ___Project___ and save the _LaTeX_ data as `<project_name>.tex` and `<project_name>.pdf`.
```sh
logbuch -mk
```

You may also pass a ___Project___ name, so Logbuch will compile only it with its contents, or pass `all` as argument and Logbuch will compile the content from all ___Projects___ you have. (In the later case, outputs will be named `all.tex` and `all.pdf`.)
```sh
logbuch -mk name of your project
```

All outputs are saved in your ___Projects___ root folder and are named with your ___Project___ name followed by `.tex` and `.pdf` for the compilation output (by default). Feel free to edit these files as you wish.

If you have an existing `.tex` file with same name as output, Logbuch will prompt you if you want to overwrite it, so you can just recompile a previous `.tex` version.

For more detailed explanation about compiling steps, please read [this section](#pandoc-conversion).

---
###### `-g/--git` option

_Warning: Bash Completion is not working properly with this option when a `git`'s option is typed after the `--`. I made a Pull Request for Click developers in order to solve this. As soon as possible I will update this._

This option is just a convenience to use `git` inside your ___Projects___ root folder without walking into it. In order to use it properly, you must pass double dashes `--` right after `-g/--git`, else Logbuch will understand any dash-started string as another option.

This option works redirecting all arguments received to your `git` command in `PATH`. For instance, if you want to check your repository status:
```sh
logbuch -g status
logbuch -g -- status
```

To use this option, Logbuch expects your ___Projects___ root folder to be a `git` repository. You can, however, create a new one using Logbuch by just typing:
```sh
logbuch -g init
logbuch -g -- add --all
logbuch -g -- commit -m "First commit."
```

This option does just call `git` plus the arguments you passed. I would suggest you to check the [wrapper code](logbuch/src/logbuch/git.py) and [git integration code](logbuch/src/logbuch/gitintegration.py) if you are not feeling safe to use it.

---
###### `-c/--conf` option

This option opens the configuration file `~/.logbuch/conf.cfg` in your text editor, so you can edit it by hand. The parameters were deeply discussed at [configuration section](#configuration).

---
###### `-h/--help` option
Finally, you can always use the `-h/--help` option to get information about Logbuch options.

---

FYI:
- ___Subject___ and ___Project___ names are allowed to have space. Their leading char will always be capitalized and the remaining lowered. Underscores will be converted to spaces. They cannot start with a `.` because they will be ignored by other Logbuch functions.
- Logbuch may handle cases that are not discussed in this README. If you get any trouble using Logbuch, please, let me know.
- Any dash-started string will be treated as an option if you do not use the double dash `--` separator. You shall use it right after the first option.

## Pandoc conversion

As Logbuch aims to be an easy-to-use and portable program, `pandoc` showed to be the best tool for text conversion, as it allows you to write your notes in many markup languages and convert them to many others.

For the default procedure defined by me when developing Logbuch, I made all tests and integration with `pandoc`'s `markdown` as input format and `latex` as output one. If you try to use any other format, please let me know whether it worked and what problems you faced through an [issue](#issues-and-desired-features).

Besides that, Logbuch uses `pandoc` at three different steps before compiling to _LaTeX_.

1. [___Subject___ conversion](#subject-conversion)
2. [___Project___ conversion](#project-conversion)
3. [Whole document conversion](#whole-document-conversion)

Each of these steps uses the logic: `pandoc template` + `pandoc YAML` + `user written content` = `pandoc converted output`. Deeply detailed information about _templates_ and _YAML metadata blocks_ can be found [here](https://pandoc.org/MANUAL.html#templates).

- `pandoc template` is a file where you describe the structure of your output text. `pandoc` accepts variables and replace them by their definition at `pandoc YAML`.
- `pandoc YAML` is a file consisting of `YAML` blocks that define variables used in `pandoc template`
- `user written content` are all text written outside these two files above and that is written in the [`pandoc_from_format`](#configuration) to be converted.

### ___Subject___ conversion

Each ___Subject___ that is created or edited through Logbuch automatically creates a `YAML` header with default variables used by the default ___Subject___ `template`. This header is created with the same name as the ___Subject___ prepending a dot `.` to it. Therefore it's a hidden file that Logbuch (~~yet~~) does not handle and you must edit it manually. This header is saved in the same path as its ___Subject___.

If you want to use other than the default `template`, you must save your own `template` at the ___Projects___ folder and name it `.subj.template.tex` (don't forget the initial `.`).

Also, you can add any variable following the `YAML` syntax and use them in the `template`, as `pandoc` defines in its documentation.

Logbuch will compile individually each ___Subject___ with the same `template` and append their output to the final buffer.

This step of conversion happens for each ___Subject___ read.

_Default template philosophy:_ Each ___Subject___ is thought as a `chapter` of a book in the _LaTeX_ terminology.

### ___Project___ conversion

Each ___Project___ will have a copy of the default ___Project___ `YAML` named `.proj.yaml` inside it. The same process described for ___Subject___ will be done. However, each ___Project___ output will come before all of its ___Subjects___.

If you want to use other than the default `template`, you must save your own `template` at the ___Projects___ folder and name it `.proj.template.tex`.

This step may not have a `body` entry in your `YAML` or `template` files, as there is no content for them editable by Logbuch (~~yet~~).

This step of conversion happens at the beginning of each new ___Project___ read.

_Default template philosophy:_ Each ___Project___ is thought as a `part` of a book in the _LaTeX_ terminology. So they will be the higher sectioning in your Lab-Book.

### Whole document conversion

After filling the buffer with all the previous conversions content, Logbuch will call `pandoc` with a completely structured `template` at this step.

At this point, there will be no more unconverted ___Subject___ in the `pandoc_from_format` format. So, this is roughly just a 'amalgamation' and restructuring step.

Logbuch will get all `metadata` written at `.meta.yaml` in your ___Projects___ root folder and append all the buffer content to it. This content will be, thus, the `body` variable inside the final `template`.

Then, Logbuch will call `pandoc` passing that `metadata+body` to the final `template` and generate the output in, e.g., `.tex` format.

The default `template` is a slightly modified version of an user contributed `template` [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template). It's a good idea to read its entire documentation and original `template` if you want to edit the default `metadata` file or even create your own `template`. It's not that hard, but you may invest some of your time learning how it works.

If you want to use other than the default `template`, you must save your own `template` at the ___Projects___ folder and name it `.proj.template.tex`.

I'm glad to receive any design tips, as I'm not that good and I know the default `template` should have improvements.

## Issues and desired features

Report any issues you may find at the [repository Issues page](https://github.com/bertolinocastro/logbuch/issues).

If you wish any new feature to be added in Logbuch, please, do not hesitate to let me know it! Use the Issues page and tell me what you want. :-)

All criticisms and suggestions are very welcome!

## Credits

- @bertolinocastro  
    Just the author of Logbuch.

- @waltercostamb  
    Mentor and author of a brilliant workshop showing all purposes of doing Lab-Book at the Academy and her structured and logic way to deal with her research annotations. For more in-deep information, check her [Lab-Book repository](https://github.com/waltercostamb/Lab-Book).

## License

© Bertolino

Licensed under the [MIT License](LICENSE.txt)
