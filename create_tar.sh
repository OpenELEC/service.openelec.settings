#!/bin/sh

git archive --format=zip tags/$1 -o service.openelec.settings-$1.zip
