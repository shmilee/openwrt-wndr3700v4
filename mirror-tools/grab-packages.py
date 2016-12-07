#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Openwrt Packages Grabber
# Copyright (C) 2016 shmilee

import os
import time
import re
import requests
import gzip
import hashlib

from multiprocessing import Pool
from contextlib import closing

import setting
from progressbar import ProgressBar
from profiles import PROFILES

DISTRIB_RELEASE = PROFILES[setting.PROFILE]['DISTRIB_RELEASE']
DISTRIB_CODENAME = PROFILES[setting.PROFILE]['DISTRIB_CODENAME']
DISTRIB_TARGET = PROFILES[setting.PROFILE]['DISTRIB_TARGET']
IPK_GROUPS = PROFILES[setting.PROFILE]['IPK_GROUPS']
DB_FILES = PROFILES[setting.PROFILE]['DB_FILES']
DB_HASH = PROFILES[setting.PROFILE]['DB_HASH']
BASEURL = '%s/%s/%s/%s/packages' % (
    setting.URL,
    PROFILES[setting.PROFILE]['DISTRIB_CODENAME'],
    PROFILES[setting.PROFILE]['DISTRIB_RELEASE'],
    PROFILES[setting.PROFILE]['DISTRIB_TARGET']
)
SAVEDIR = setting.SAVEDIR

if DB_HASH == 'SHA256sum':
    hashfun = hashlib.sha256
elif DB_HASH == 'MD5Sum':
    hashfun = hashlib.md5
else:
    print('==> Invalid Hash Algorithm: %s' % DB_HASH)
    raise NameError("Profiles.PROFILES['%s']['DB_HASH']"
                    % setting.PROFILE)

print('==> fetch url : %s\n==> save directory : %s'
      % (BASEURL, SAVEDIR))


def download_helper(url, outfile, ha, title):
    if ha and os.path.exists(outfile) \
            and ha == hashfun(open(outfile, 'rb').read()).hexdigest():
        print('\033[32m[%s]\033[0m exists, pass.' % title)
        return None

    shot_title = title.split(sep=r') ')[1]
    try:
        with closing(requests.get(url, **setting.REQUESTS_KWARGS)) as rp:
            chunk_size = 1024
            content_size = int(rp.headers['content-length'])
            progress = ProgressBar(title, total=content_size, unit="KB",
                                   chunk_size=chunk_size,
                                   run_status="正在下载",
                                   fin_status="下载完成")
            with open(outfile, "wb") as file:
                for data in rp.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
    except Exception as err:
        print('\033[31m[Download %s Error]\033[0m' % shot_title, err)
        return (url, shot_title)
    finally:
        if not os.path.exists(outfile):
            print('\033[31m[%s]\033[0m Download failed!' % title)
            return (url, shot_title)
        if ha and ha != hashfun(open(outfile, 'rb').read()).hexdigest():
            print('\033[31m[%s]\033[0m BROKEN!' % title)
            return (url, shot_title)
        return None


def download_package_db(psize):
    start = time.time()

    print('==> [DB] Task: Download package databases ...')
    if IPK_GROUPS:
        db_files = ['%s/%s' % (g, d) for g in IPK_GROUPS for d in DB_FILES]
        for g in IPK_GROUPS:
            if not os.path.exists(SAVEDIR + '/' + g):
                os.makedirs(SAVEDIR + '/' + g)
    else:
        db_files = DB_FILES
        if not os.path.exists(SAVEDIR):
            os.makedirs(SAVEDIR)

    p = Pool(psize)
    db_fails = []
    for i, d in enumerate(db_files):
        url = BASEURL + '/' + d
        outfile = SAVEDIR + '/' + d
        title = r'(%' + str(len(str(len(db_files)))) + r's/%s) %s'
        title = title % (i + 1, len(db_files), d)
        result = p.apply_async(
            download_helper, args=(url, outfile, None, title))
        db_fails.append(result)
    p.close()
    p.join()

    for db_fail in db_fails:
        if db_fail.get():
            raise Exception('==> \033[31m[DB] Task Failed!\033[0m')

    if IPK_GROUPS:
        for g in IPK_GROUPS:
            if g == 'oldpackages':
                encoding = 'ISO-8859-2'  # 坑 14.07
            else:
                encoding = 'utf-8'
            with gzip.open('%s/%s/Packages.gz' % (SAVEDIR, g), 'rb') as db:
                data = db.read()
            with open('%s/%s/Packages' % (SAVEDIR, g), 'w') as db:
                db.write(data.decode(encoding))
    else:
        with gzip.open('%s/Packages.gz' % SAVEDIR, 'rb') as db:
            data = db.read()
        with open('%s/Packages' % SAVEDIR, 'w') as db:
            db.write(data.decode('ISO-8859-2'))

    end = time.time()
    print('==> [DB] Task runs %0.2f seconds.' % (end - start))


def download_package_group(psize, group):
    start = time.time()

    if group:
        print('==> [%s] Task: Download packages of %s ...' % (group, group))
        print(' -> Analyzing %s database ...' % group)
        db_file = SAVEDIR + '/' + group + '/Packages'
        url_pre = BASEURL + '/' + group + '/'
        out_pre = SAVEDIR + '/' + group + '/'
        broken = os.path.split(SAVEDIR)[0] + '/' + group + '-broken-ipks'
    else:
        print('==> [IPK] Task: Download packages ...')
        print(' -> Analyzing database ...')
        db_file = SAVEDIR + '/Packages'
        url_pre = BASEURL + '/'
        out_pre = SAVEDIR + '/'
        broken = os.path.split(SAVEDIR)[0] + '/' + 'broken-ipks'

    ipk_files = []
    ipk_hashs = []
    with open(db_file, 'r') as db:
        data = db.read()
        for match in re.findall(r'Filename: .*\.ipk', data):
            ipk_files.append(re.sub(r'Filename: (.*\.ipk)', r'\1', match))
        for match in re.findall(r'%s: .*' % DB_HASH, data):
            ipk_hashs.append(re.sub(r'%s: (.*)' % DB_HASH, r'\1', match))

    p = Pool(psize)
    if group:
        title_tmp = r'(%' + str(len(str(len(ipk_files)))) + r's/%s) %s/%s'
    else:
        title_tmp = r'(%' + str(len(str(len(ipk_files)))) + r's/%s) %s'
    ipk_fails = []
    for i, val in enumerate(zip(ipk_files, ipk_hashs)):
        url = url_pre + val[0]
        outfile = out_pre + val[0]
        if group:
            title = title_tmp % (i + 1, len(ipk_files), group, val[0])
        else:
            title = title_tmp % (i + 1, len(ipk_files), val[0])
        result = p.apply_async(
            download_helper, args=(url, outfile, val[1], title))
        ipk_fails.append(result)
    p.close()
    p.join()

    with open(broken, "w") as file:
        for result in ipk_fails:
            if result.get():
                file.write('%s -> %s\n' % result.get())

    end = time.time()
    if group:
        print('==> [%s] Task runs %0.2f seconds.' % (group, (end - start)))
    else:
        print('==> [IPK] Task runs %0.2f seconds.' % (end - start))

    if not os.path.getsize(broken):
        os.remove(broken)
    else:
        return broken


def main():
    mainstart = time.time()

    download_package_db(3)

    broken_list = []
    if IPK_GROUPS:
        for group in IPK_GROUPS:
            broken = download_package_group(setting.PSIZE, group)
            if broken:
                broken_list.append(broken)
    else:
        broken = download_package_group(setting.PSIZE, None)
        if broken:
            broken_list.append(broken)
    if broken_list:
        print('==> See the broken ipks in:')
        for broken in broken_list:
            print(' -> %s' % broken)

    mainend = time.time()
    print('==> [ALL] Tasks run %0.2f seconds.' % (mainend - mainstart))

if __name__ == "__main__":
    main()
