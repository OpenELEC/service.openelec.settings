#!/bin/sh

git archive --format=tar.gz --prefix=OpenELEC-settings-$1/ tags/$1 -o OpenELEC-settings-$1.tar.gz
