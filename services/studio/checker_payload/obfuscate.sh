#!/bin/bash

#INJECT_POS=$(grep -a -b '//obfuscator_hint' src_main.c | awk -F ':' '{print $1}')
#echo "Inject position $INJECT_POS"

DUMMY_DATA=$(./generate_dummy_code.py)


SRC_FILE=$(<src_main.c)
echo "${SRC_FILE//obfuscator_inject_pos/$DUMMY_DATA}" > main.c

