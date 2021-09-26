#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import importlib.util


def read_file(infile):
    try:
        with open(infile) as file:
            data = file.read()
        return data
    except Exception as err:
        print('\033[31m[Error]\033[0m %s' % err)
        return None


def generate_file(dest, contents, templatedir):
    '''
    dest: file path in root, like etc/xxx
    contents: list of string and template files, in order, like
        str, "string"
        tuple, ('filepath in templatedir', ('replace old', 'new'), ('old', 'new'))
        tuple, (':SUB:', ('replace old', 'new'), ('old', 'new'))

    '''
    print('==> generating %s ...' % dest)
    temp = ''
    for c in contents:
        if isinstance(c, str):
            temp = temp + c
            print(' -> ADD: %s' % c)
        elif isinstance(c, tuple):
            cfile = os.path.join(templatedir, c[0])
            if os.path.isfile(cfile):
                print(' -> ADD FILE: %s' % cfile)
                indata = read_file(cfile)
                for old, new in c[1:]:
                    indata = indata.replace(old, new)
                    print('   -> SUBS: %s\n   ->   TO: %s' % (old, new))
                temp = temp + indata
            elif c[0] == ':SUB:':
                for old, new in c[1:]:
                    temp = temp.replace(old, new)
                    print('   -> SUBS: %s\n   ->   TO: %s' % (old, new))
            else:
                print(' -> ignore FILE: %s' % c[0])
        else:
            print(' -> Unknown content type: %s.' % type(c))
    try:
        destdir = os.path.split(dest)[0]
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        with open(dest, "w") as file:
            file.write(temp)
    except Exception as err:
        print('\033[31m[Error]\033[0m %s' % err)


def deploy(all_myfiles, templatedir, outdir='myfiles_for_image'):
    print('==> Files TODO:\n')
    for k in sorted(all_myfiles.keys()):
        print(k)
    print('\n==> BEGIN\n')
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    for k in sorted(all_myfiles.keys()):
        dest = os.path.join(outdir, k)
        contents = all_myfiles[k]
        generate_file(dest, contents, templatedir)
    print('\n==> Done.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        setfile = sys.argv[1]
    else:
        setfile = './myfiles-secret-example.py'
    if os.path.isfile(setfile):
        print('==> Reading setting file: %s ...' % setfile)
        spec = importlib.util.spec_from_file_location('setting', setfile)
        setting = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setting)
        deploy(setting.all_myfiles, setting.templatedir, setting.outdir)
    else:
        print('==> Lost setting file!')
