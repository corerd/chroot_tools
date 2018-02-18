#!/usr/bin/env python

'''Copy binary and its dynamically linked shared libraries into chroot jail,
creating also the necessary sub directories.

Ref: Use otool recursively to find shared libraries needed by an app
     https://stackoverflow.com/a/1517652
'''
from __future__ import print_function

import os
import sys
import subprocess
from shutil import copy


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_highlight(msg):
    print('%s==>%s %s%s%s' %
            (bcolors.OKBLUE, bcolors.ENDC, bcolors.BOLD, msg, bcolors.ENDC))


def get_relative_path(root_path):
    if root_path.startswith(os.sep):
        return root_path[1:]
    return root_path


def otool(object_file_path):
    '''Generator of the shared libraries path names that the object file uses,
    as well as the shared library ID if the file is a shared library.

    Returns normalized absolutized version of the library file path.
    '''
    o = subprocess.Popen(['/usr/bin/otool', '-L', object_file_path], stdout=subprocess.PIPE)
    for l in o.stdout:
        if l[0] == '\t':
            #yield l.split(' ', 1)[0][1:]
            library_path = os.path.abspath(l.split(' ', 1)[0][1:])
            if os.path.exists(get_relative_path(library_path)) is not True:
                yield library_path


def cp_dependencies(binary_file_path):
    need = set([binary_file_path])
    src_libraries_paths = set()
    dst_directories = set([])

    while need:
        needed = set(need)
        need = set()
        for f in needed:
            need.update(otool(f))
        src_libraries_paths.update(needed)
        need.difference_update(src_libraries_paths)

    if len(src_libraries_paths) == 0:
        print('No dependencies to copy for %s' % binary_file_path)
        return 1

    print_highlight('This script will copy %s and its dependencies:' % binary_file_path)
    for f in sorted(src_libraries_paths):
        dst_path = get_relative_path(os.path.dirname(f))
        if os.path.exists(dst_path) is not True:
            dst_directories.update([dst_path])
        print(f)

    if len(dst_directories) > 0:
        print_highlight('The following new directories will be created:')
        for d in sorted(dst_directories):
            print(d)

    user_choice = raw_input('\nDo you want to continue [y/N]? ')
    if user_choice.strip().lower() != 'y':
        print('Aborted by the user')
        return 1

    print('Installing...')
    for d in sorted(dst_directories):
        print('Create directory %s' % d)
        os.makedirs(d)
    for src_file_path in sorted(src_libraries_paths):
        dst_file_path = get_relative_path(src_file_path)
        print('Copy %s in %s' % (src_file_path, dst_file_path))
        copy(src_file_path, dst_file_path)  # NOTABLE: copy also the permissions


def main(argv, argc):
    if argc != 2:
        print('USAGE: cpdylib OBJECT_FILE')
        return -1
    exit_code = cp_dependencies(argv[1])
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv, len(sys.argv)))
