#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Openwrt Packages Grabber
# Copyright (C) 2016 shmilee

import os, time, re
import requests
import hashlib

from multiprocessing import Pool
from urllib import response
from contextlib import closing

# 15.05.1 /etc/openwrt_release
DISTRIB_ID       = "OpenWrt"
DISTRIB_RELEASE  = "15.05.1"
DISTRIB_REVISION = "r48532"
DISTRIB_CODENAME = "chaos_calmer"
DISTRIB_TARGET   = "ar71xx/nand"

# package group
IPKGRPS=('base', 'luci', 'management', 'packages', 'routing',
         #'telephony' #坑, > 400M
         )

# download site, mirror
#URL = 'http://downloads.openwrt.org'
URL = 'http://openwrt.proxy.ustclug.org'

#prefix for directory to save all the packages
SAVE_PREFIX = 'ipks-'

BASEURL = URL + '/' + DISTRIB_CODENAME + '/' + DISTRIB_RELEASE \
          + '/' + DISTRIB_TARGET + '/packages/'
SAVEDIR = './' + SAVE_PREFIX + DISTRIB_RELEASE \
          + '/' + DISTRIB_TARGET + '/packages/'

if not os.path.exists(SAVEDIR):
    os.makedirs(SAVEDIR)

print('==> fetch url : %s\n==> save directory : %s'
      % (BASEURL, SAVEDIR))

# ref: https://www.zhihu.com/question/41132103
class ProgressBar(object): #{{{

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq,
                             self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)
#}}}


def download_helper(url, outfile, sha):
    if not os.path.exists(os.path.split(outfile)[0]):
        os.makedirs(os.path.split(outfile)[0])
    title = url.split(DISTRIB_TARGET+'/packages/')[-1]
    if sha and os.path.exists(outfile) \
           and sha == hashlib.sha256(open(outfile, 'rb').read()).hexdigest():
        print('\033[32m[%s]\033[0m exists, pass.' % title)
        return None
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        progress = ProgressBar(title, total=content_size, unit="KB",
                               chunk_size=chunk_size,
                               run_status="正在下载",
                               fin_status="下载完成")
        with open(outfile, "wb") as file:
           for data in response.iter_content(chunk_size=chunk_size):
               file.write(data)
               progress.refresh(count=len(data))
    if sha and sha != hashlib.sha256(open(outfile, 'rb').read()).hexdigest():
        print('\033[31m[%s]\033[0m BROKEN!' % title)
        return (url, title)

def download_package_db(psize):
    print('==> [DB] Task: Download package databases ...')
    start = time.time()
    p = Pool(psize)
    for group in IPKGRPS:
        for f in ('/Packages', '/Packages.gz', '/Packages.sig'):
            url = BASEURL + group + f
            outfile = SAVEDIR + group + f
            p.apply_async(download_helper, args=(url, outfile, None))
    p.close()
    p.join()
    end = time.time()
    print('==> [DB] Task runs %0.2f seconds.' % (end - start))

def download_package_group(psize, group):
    print('==> [%s] Task: Download packages of %s ...' % (group, group))
    start = time.time()
    print(' -> Analyzing %s database ...' % group)
    ipk_files = []
    ipk_shas  = []
    ipk_fails = []
    if group == 'oldpackages':
        encode='ISO-8859-2' #坑
    else:
        encode='utf-8'
    with open(SAVEDIR + group + '/Packages', 'r', encoding = encode) as db:
        data = db.read()
        for match in re.findall(r'Filename: .*\.ipk', data):
            ipk_files.append(re.sub(r'Filename: (.*\.ipk)', r'\1', match))
        for match in re.findall(r'SHA256sum: .*', data):
            ipk_shas.append(re.sub(r'SHA256sum: (.*)', r'\1', match))
    p = Pool(psize)
    for i,sha in zip(ipk_files,ipk_shas):
        url = BASEURL + group + '/' + i
        outfile = SAVEDIR + group + '/' + i
        result = p.apply_async(download_helper, args=(url, outfile, sha))
        ipk_fails.append(result)
    p.close()
    p.join()
    with open(group + '-Broken-ipks', "w") as file:
        for result in ipk_fails:
            if result.get():
                file.write('%s -> %s\n' % result.get())
    if not os.path.getsize(group + '-Broken-ipks'):
        os.remove(group + '-Broken-ipks')
    end = time.time()
    print('==> [%s] Task runs %0.2f seconds.' % (group, (end - start)))

def main():
    mainstart = time.time()
    download_package_db(4)
    for group in IPKGRPS:
        download_package_group(40, group)
    mainend = time.time()
    print('==> [ALL] Tasks run %0.2f seconds.' % (mainend - mainstart))

if __name__ == "__main__":
    main()
