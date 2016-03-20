#!/bin/bash

function join {
 local IFS="$1"; shift; echo "$*"; 
}

function find_projects {
 git log --pretty=oneline | egrep -oe"[A-Z]{3,15}[ -][[:digit:]]{3,5}" | sed 's/[ -].*//g' \
 | sort | uniq -c | grep -v '\s[0-9] ' | cut -f 5 -d' '
}

function commit_to_issuekey {
 ISSUE_KEY="${1}-[[:digit:]]{1,5}"

 git log --pretty=oneline \
 | tr --delete '\[\]' \
 | sed "s/\($ISSUE_KEY\).*?\($ISSUE_KEY\)/\1 \2/g" \
 | grep --only-matching -i -E "[[:alnum:]]{40}( $ISSUE_KEY)+" \
 # | sort --general-numeric-sort --key=2 --field-separator=-
}

WORKDIR=${1:-.}
cd $WORKDIR

PROJECTS=$(find_projects)
commit_to_issuekey "($(join '|' $PROJECTS))"
echo "Projects found: $(join ' ' $PROJECTS)" | grep --color '.*' > /dev/stderr
