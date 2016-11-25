#!/bin/bash
# https://github.com/Wind4/vlmcsd/
# http://rgho.st/6G8wYxwnX -> vlmcsd-svn812-2015-08-30-Hotbird64.7z
# 7z key: 2015
echo "==> Key can be found here:"
echo " -> https://technet.microsoft.com/en-us/library/jj612867.aspx"
echo
mkdir ./test/
# for DB120
find ./binaries -name "vlmcsd-mips16-*" -exec cp {} ./test/ -iv \;
find ./binaries -name "vlmcsd-mips32r1-*" -exec cp {} ./test/ -iv \;
find ./binaries -name "vlmcsd-mips32-*" -exec cp {} ./test/ -iv \;
cp ./vlmcsd.ini ./test/
rm ./test/*-Fritzbox-* ./test/*-glibc
