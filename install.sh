#!/bin/bash
printf "
Automated installer.
It uses python 3.7 or higher.

You may pass python executable as inline var.
For instance: PYTHON=python3.7 ./install.sh

"
if [[ -z $PYTHON ]]; then
  PYTHON=python3
fi

which ${PYTHON} &> /dev/null
if [[ 1 -eq $? ]];then
  echo "${PYTHON} does not exist as a command in your system!"
  exit
fi

$PYTHON -c "
import sys
sys.exit(sys.version_info < (3,7))
"
if [[ $? -eq 1 ]];then
  echo "Wrong python version. It must be 3.7 or higher."
  echo "Alternatively, you can set inline PYTHON var. For example: PYTHON=python3.7 ./install.sh"
else
  version=$($PYTHON -c 'import sys;print("%s.%s"%sys.version_info[0:2])')
  echo -e "Installing Logbuch...\n"
  python${version} -m pip install .
fi
