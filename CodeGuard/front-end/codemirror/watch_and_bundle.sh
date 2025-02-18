#!/bin/bash

set -ex

reflex -g editor.js -- sh -c \
    'npx rollup editor.js -f iife -o ../static/js/cm6.bundle.js -p @rollup/plugin-node-resolve --output.name cm6 && \
     echo ...done'
