#!/bin/sh
set -eu

./autogen.sh

./configure --disable-lockfiles "$@"

make clean
make
