#!/bin/bash
openssl dgst -sha1 -binary < "./install/MakeHuman_1.0_alpha4_osx.pkg.zip" | \
    openssl dgst -dss1 -sign <(security find-generic-password -g -s "Sparkle Private Key 1" 2>&1 1>/dev/null | \
    perl -pe '($_) = /"(.+)"/; s/\\012/\n/g') | openssl enc -base64
