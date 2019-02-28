#!/bin/bash
printf "
Automated demo installer.
It uses python's 3 or higher venv module.

It must be sourced, not directly executed. For instance: source ./demo_install.sh

You may pass python executable as inline var.
For instance: PYTHON=python3.7 source ./demo_install.sh

"
# checking for source or prevent execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  exit
fi

if [[ -z $PYTHON ]]; then
  PYTHON=python3
fi

which ${PYTHON} &> /dev/null
if [[ 1 -eq $? ]];then
  echo "${PYTHON} does not exist as a command in your system!"
  return
fi

echo -e "Starting virtual environment creation...\n"

$PYTHON -c "
import sys
sys.exit(sys.version_info < (3,7))
"

if [[ $? -eq 1 ]];then
  echo "Wrong python version. It must be 3.7 or higher."
  echo "Alternatively, you can set inline PYTHON var. For example: PYTHON=python3.7 source ./demo_install.sh"
else
  version=$($PYTHON -c 'import sys;print("%s.%s"%sys.version_info[0:2])')
  dpkg -s python${version}-venv > /dev/null
  if [[ 1 -eq $? ]];then
    echo "python${version}-venv package not found!"
    echo "You must install it or a higher version"
  else
    $PYTHON -m venv venv
    echo "Python virtual environment created."
    . venv/bin/activate
    echo -e "Installing Logbuch in actual virtual environment...\n"
    python${version} -m pip install --editable .
  fi

fi
