Setting Up a chroot Jail
========================

1. Create a bin directory in jail and copy /bin/sh to this directory.

2. Because sh binary is dynamically linked to shared libraries,
   you need to copy these libraries into jail /lib as well.
   Use otool to display the shared libraries dependencies,
   and copy the necessary libraries.

   [A Practical Guide to UNIX for Mac OS X Users](https://books.google.it/books?id=o9K8KEQic5sC&lpg=PA462&ots=lYN_447djB&dq=macos%20chroot%20fail&hl=it&pg=PA462#v=onepage&q=macos%20chroot%20fail&f=false)

   [Creating basic chroot environment](https://linuxconfig.org/how-to-automatically-chroot-jail-selected-ssh-user-logins).

1. Also copy /usr/lib/dyld to your chroot jail to get the dynamic linker.
   If that is not present, then attempting to execute anything in the chroot jail
   will fail without any error other than
       Killed: 9

   https://stackoverflow.com/a/34116191


Other References
----------------

[Setting Up a Chroot user/group for SSH](https://rileyshott.wordpress.com/2013/01/14/mac-setting-up-a-chroot-usergroup-for-ssh/)

[Mac OS X El Capitan Installer Removes Custom Group ID And Membership](https://funcptr.net/2015/10/02/mac-os-x-el-capitan-installer-removes-custom-group-id-and-membership/)
