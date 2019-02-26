#!/bin/bash

PYTHON=python3

# automated install script

$PYTHON -c << EOF
import sys
sys.exit(sys.version_info < (3.7))
EOF

echo $?
