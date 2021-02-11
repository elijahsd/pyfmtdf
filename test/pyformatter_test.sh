#!/bin/bash

# Dumps the difference between the original script and a rendered version.
# w3m serves as a renderer

if [ -z "$1" ]; then
	echo "Usage: $0 filename"
	exit
fi

cat $1 | sed 's/\t/    /g' > /tmp/pyformatter.in

python3 main.py $1 > /tmp/pyformatter.html

cat /tmp/pyformatter.html | w3m -dump -T text/html > /tmp/pyformatter.out
truncate -s-1 /tmp/pyformatter.out

# firefox /tmp/pyformatter.html

# meld /tmp/pyformatter.in /tmp/pyformatter.out

# lynx -dump /tmp/pyformatter.html > /tmp/pyformatter.out

diff /tmp/pyformatter.in /tmp/pyformatter.out

# links -driver x -force-html /tmp/pyformatter.html

# python3 main.py $1 | firefox "data:text/html;base64,$(base64 -w 0 <&0)"
