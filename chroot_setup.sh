#!/usr/bin/env bash

# Basic chroot jail set up with just sh shell
# Ref: https://books.google.it/books?id=o9K8KEQic5sC&lpg=PA462&ots=lYN_447djB&dq=macos%20chroot%20fail&hl=it&pg=PA462#v=onepage&q=macos%20chroot%20fail&f=false

# Copy sh and its dynamically linked shared libraries into jail,
# creating the necessary sub directories.
python cpdylib.py /bin/sh
rc=$?
if [[ $rc != 0 ]]; then
  exit $rc
fi

# Copy /usr/lib/dyld into chroot jail to get the dynamic linker.
cp /usr/lib/dyld usr/lib/.
echo "Done!"
