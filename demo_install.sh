#!/bin/bash

PYTHON=python3

# automated install script

$PYTHON -c << EOF
import sys
sys.exit(sys.version_info < (3.7))
EOF

echo $?

# demo install using pyenv
sudo apt install python3.7-venv
python3.7 -m venv venv

. teste_env/bin/activate
pip3 install --editable .
