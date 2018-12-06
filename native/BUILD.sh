#!/bin/sh
set -eu

./autogen.sh

./configure "$@"

make clean
make
