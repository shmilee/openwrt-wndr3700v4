#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from myfiles_secret import outdir, templatedir, all_templates, all_myfiles


print('==> Templates:\n%s' % all_templates)
print('==> Files TODO:\n')
for k in sorted(all_myfiles.keys()):
    print(k)

print('\n==> BEGIN\n')

if os.path.exists(outdir):
    shutil.rmtree(outdir)
os.makedirs(outdir)


def read_file(infile):
    try:
        with open(infile) as file:
            data = file.read()
    except Exception as err:
        print('\033[31m[Error]\033[0m %s' % err)
    return data

for k in sorted(all_myfiles.keys()):
    template = '%s/%s' % (templatedir, k)
    outfile = '%s/%s' % (outdir, k)
    filedir = os.path.split(outfile)[0]
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    print('==> %s -> %s' % (template, outfile))
    temp = read_file(template)

    for task in all_myfiles[k]:
        action = task[0]
        if action == 'ADD':
            temp = temp + task[1]
            print(' -> ADD: %s' % task[1])
        elif action == 'REPLACE':
            for olddata, newdata in task[1:]:
                temp = temp.replace(olddata, newdata)
                print(' -> REPLACE: %s\n -> TO: %s' % (olddata, newdata))
        elif action == 'ADDFILE':
            indata = read_file(task[1])
            print(' -> ADDFILE: %s' % task[1])
            for olddata, newdata in task[2:]:
                indata = indata.replace(olddata, newdata)
                print('   -> REPLACE: %s\n   -> TO: %s' % (olddata, newdata))
            temp = temp + indata
        else:
            print(' -> Unknown ACTION %s.' % action)

    try:
        with open(outfile, "w") as file:
            file.write(temp)
    except Exception as err:
        print('\033[31m[Error]\033[0m %s' % err)

print('\n==> Done.')
