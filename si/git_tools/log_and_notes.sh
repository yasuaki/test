#!/bin/sh

gitdir=$1
branch=$2
range=$3

export GIT_DIR=$gitdir
notes_ref=refs/notes/$(git rev-parse --symbolic-full-name $branch | sed 's#^refs/##')

GIT_NOTES_REF=$notes_ref	\
git log $range
