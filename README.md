Setting Up a chroot Jail
========================

1. Create a bin directory in jail and copy /bin/sh to this directory.

2. Because sh binary is dynamically linked to shared libraries,
   you need to copy these libraries into jail /lib as well.
   Use otool to display the shared libraries dependencies,
   and copy the necessary libraries.

   Ref: [A Practical Guide to UNIX for Mac OS X Users](https://books.google.it/books?id=o9K8KEQic5sC&lpg=PA462&ots=lYN_447djB&dq=macos%20chroot%20fail&hl=it&pg=PA462#v=onepage&q=macos%20chroot%20fail&f=false)

1. Also copy /usr/lib/dyld to your chroot jail to get the dynamic linker.
   If that is not present, then attempting to execute anything in the chroot jail
   will fail without any error other than
       Killed: 9

   Ref: https://stackoverflow.com/a/34116191
