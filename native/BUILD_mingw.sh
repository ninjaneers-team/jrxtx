#!/bin/bash
set -euxo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export LIB_EXTENSION=dll
./autogen.sh

./configure --target=x86_64-w64-mingw32 --host=x86_64-w64-mingw32

make clean
make LDFLAGS="-no-undefined -lpthread -lmingw32" CFLAGS="-I${DIR}/src"
