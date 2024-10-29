#!/bin/bash

cd gredu-dcj/
aclocal
autoconf
autoheader
automake -a
./configure
make