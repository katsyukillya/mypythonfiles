#!/usr/bin/env/python3

"""
    This program creates a simple file tree that starts at the directory of the User
    choice.
    In case the start_at directory does not exist, the program gracefully ends
    without throwing an exception.
    If the user provides the absolute path in Windows-like format: C:\Program Files\...
    this will result in the absolute file tree where the directories will be placed
    on absolute branches. If the UNIX-like path is provided for the start_at string,
    the tree will have relative branching.
"""
#    Created by I. Katsyuk

import os


def GatherTree(start_at):
    """Returns a dictionary of all the parts to files and
    directories in the directory structure starting at
    start_at. The keys are the paths, the values are either
    'directory' or 'file'
    """
    node_d = {}
    for (this_dir, dir_names, file_names) in os.walk(start_at):
        node_d[this_dir] = 'directory'
        for f_name in file_names:
            node_d[os.path.join(this_dir, f_name)] = 'file'
    return node_d


def Tree(start_at):
    """Prints the directory/file structure starting at start_at."""
    node_d = GatherTree(start_at)
    directories = 0
    files = 0
    for node in sorted(node_d):
        path, name = os.path.split(node)
        slashes = path.count(os.sep)
        print("  | " * slashes, end='')
        if path:
            print(" |--", end='')
        if node_d[node] == 'directory':
            print(os.sep + name)
            directories += 1
        else:
            print(name)
            files += 1

    print()
    print("%d directories, %d files" % (directories, files))


def main():
    start_at = input("Tree to start at wich directory? ")
    Tree(start_at)


if __name__ == '__main__':
    main()
