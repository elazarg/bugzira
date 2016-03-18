#!/bin/bash
WORKDIR=${1:-.}
PROJECT=${2:-$(basename $WORKDIR)}
BUG_ID="$PROJECT-[[:digit:]]{1,5}"
SHA1='[[:alnum:]]{40}'

cd $WORKDIR 

git log --pretty=oneline 										\
	| tr --delete '\[\]'										\
	| sed "s/\($BUG_ID\).*?\($BUG_ID\)/\1 \2/g"					\
	| grep --only-matching -i -E "$SHA1( $BUG_ID)+"				\
	| sort --general-numeric-sort --key=2 --field-separator=-