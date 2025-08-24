#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 shmilee

import os
import time
import re
import gzip
import hashlib
import requests
from multiprocessing import Pool
from contextlib import closing
from urllib.request import Request, urlopen

import setting


class ProgressBar(object):
    # ref: https://www.zhihu.com/question/41132103

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
                             self.count / self.chunk_size, self.unit, self.seq,
                             self.total / self.chunk_size, self.unit)
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


# Profiles for devices, Openwrt releases >=17.01
# target: default
target_release_default = dict(
    # get from /etc/openwrt_release
    # required: release, 17.01.5
    DISTRIB_RELEASE=None,
    # required: device-board, ar71xx/nand
    DISTRIB_TARGET=None,
    # packages group, >=17.01 : core -> packages
    IPK_GROUPS=('packages',),
    # core packages/database, 'Packages.gz'
    # decompress 'Packages.gz' -> 'Packages'
    # 'Packages.sig', check signature of database
    DB_FILES=('Packages.gz', 'Packages.sig'),
    # packages Hash Algorithm, verify the ipk file
    DB_HASH='SHA256sum',
    # URL/ + releases/17.01.5/targets/ar71xx/nand/packages + /Packages.gz
    PATH_REMOTE=r'releases/{DISTRIB_RELEASE}/targets/{DISTRIB_TARGET}/{IPK_GROUP}',
    # PWD/ + openwrt-17.01.5/targets/ar71xx/nand/packages + /Packages.gz
    PATH_LOCAL=r'./openwrt-{DISTRIB_RELEASE}/targets/{DISTRIB_TARGET}/{IPK_GROUP}',
)
target_snapshot_default = dict(
    # required: release, always 'SNAPSHOT'
    DISTRIB_RELEASE='SNAPSHOT',
    # required: device-board
    DISTRIB_TARGET=None,
    # required: kmods versions
    # core -> packages, kmods -> kmods/{kernel_version}-{git_version}
    IPK_GROUPS=('packages', 'kmods/xx-xx'),
    DB_FILES=('Packages.gz', 'Packages.sig'),
    DB_HASH='SHA256sum',
    # core: snapshots/targets/ar71xx/nand/packages
    PATH_REMOTE=r'snapshots/targets/{DISTRIB_TARGET}/{IPK_GROUP}',
    PATH_LOCAL=r'./openwrt-snapshots/targets/{DISTRIB_TARGET}/{IPK_GROUP}',
)

# package: default
package_release_default = dict(
    # required: release, 17.01
    DISTRIB_RELEASE=None,
    # required: cpu-arch, mips_24kc
    DISTRIB_ARCH=None,
    # packages group
    IPK_GROUPS=('base', 'luci', 'packages', 'routing', 'telephony'),
    DB_FILES=('Packages.gz', 'Packages.sig'),
    DB_HASH='SHA256sum',
    # URL/ + releases/packages-17.01/mips_24kc/base + /Packages.gz
    PATH_REMOTE=r'releases/packages-{DISTRIB_RELEASE}/{DISTRIB_ARCH}/{IPK_GROUP}',
    # PWD/ + openwrt-packages-17.01/mips_24kc/base + /Packages.gz
    PATH_LOCAL=r'./openwrt-packages-{DISTRIB_RELEASE}/{DISTRIB_ARCH}/{IPK_GROUP}',
)
package_snapshot_default = dict(
    # required: release, always 'SNAPSHOT'
    DISTRIB_RELEASE='SNAPSHOT',
    # required: cpu-arch
    DISTRIB_ARCH=None,
    # packages group
    IPK_GROUPS=('base', 'luci', 'packages', 'routing', 'telephony'),
    DB_FILES=('Packages.gz', 'Packages.sig'),
    DB_HASH='SHA256sum',
    # URL/ + snapshots/packages/mips_24kc/base + /Packages.gz
    PATH_REMOTE=r'snapshots/packages/{DISTRIB_ARCH}/{IPK_GROUP}',
    # PWD/ + openwrt-packages-snapshots/mips_24kc/base + /Packages.gz
    PATH_LOCAL=r'./openwrt-packages-snapshots/{DISTRIB_ARCH}/{IPK_GROUP}',
)


def get_profile(p):
    '''
    combine profile-default and profile-setting
    required profile keys: PATH_COUPLE, DB_FILES, DB_HASH
    '''
    if p.get('DISTRIB_TARGET', None):
        if p.get('DISTRIB_RELEASE') == 'SNAPSHOT':
            profile = target_snapshot_default.copy()
        else:
            profile = target_release_default.copy()
    else:
        if p.get('DISTRIB_RELEASE') == 'SNAPSHOT':
            profile = package_snapshot_default.copy()
        else:
            profile = package_release_default.copy()
    profile.update(p)
    profile['PATH_COUPLE'] = [
        (profile['PATH_REMOTE'].format(IPK_GROUP=g, **profile),
         profile['PATH_LOCAL'].format(IPK_GROUP=g, **profile))
        for g in profile['IPK_GROUPS']
    ]
    return profile


def get_content_length(response):
    if 'Content-Length' in response.headers:
        return int(response.headers['content-length'])
    # fallback
    headers = setting.REQUESTS_KWARGS['headers']
    timeout = setting.REQUESTS_KWARGS['timeout']
    rqst = Request(response.request.url, headers=headers, method='HEAD')
    resp = urlopen(rqst, timeout=timeout)
    return int(resp.headers['Content-Length'])

class Grabber(object):
    '''Openwrt Packages Grabber'''

    def __init__(self, profile):
        self.profile = profile
        try:
            self.path_couple = profile.get('PATH_COUPLE')
            self.db_files = profile.get('DB_FILES')
        except Exception:
            raise ValueError('Lost PATH_COUPLE or DB_FILES in profile!')
        self.db_hash = profile.get('DB_HASH', None)
        if self.db_hash == 'SHA256sum':
            self.db_hash_fun = hashlib.sha256
        else:
            raise ValueError('Invalid Hash Algorithm: %s' % self.db_hash)
        print('==> [All] Tasks:')
        for c in self.path_couple:
            print('    %s --> %s' % c)

    @staticmethod
    def _download(url, out, order, name, hashfun, hashstr):
        '''return None, or (error url, local path)'''
        title = '(%s) %s' % (order, name)
        if (hashstr and os.path.exists(out)
                and hashstr == hashfun(open(out, 'rb').read()).hexdigest()):
            print('\033[32m[%s]\033[0m exists, pass.' % title)
            return None
        try:
            with closing(requests.get(url, **setting.REQUESTS_KWARGS)) as rp:
                chunk_size = 1024
                content_size = get_content_length(rp)
                progress = ProgressBar(title, total=content_size, unit="KB",
                                       chunk_size=chunk_size,
                                       run_status="正在下载",
                                       fin_status="下载完成")
                with open(out, "wb") as file:
                    for data in rp.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        progress.refresh(count=len(data))
        except Exception as err:
            print('\033[31m[Download %s Error]\033[0m' % name, err)
            return (url, out)
        finally:
            if not os.path.exists(out):
                print('\033[31m[%s]\033[0m Download failed!' % name)
                return (url, out)
            if (hashstr and
                    hashstr != hashfun(open(out, 'rb').read()).hexdigest()):
                print('\033[31m[%s]\033[0m BROKEN!' % name)
                return (url, out)
            return None

    @staticmethod
    def _check_sign(outsig):
        if not setting.USIGN_CMD:
            return None
        out, ext = os.path.splitext(outsig)
        if ext != '.sig':
            return None
        if os.path.exists(outsig) and os.path.exists(out):
            return not os.system(setting.USIGN_CMD + ' ' + out)
        else:
            return None

    def download_package_group(self, remote, local):
        '''
        return False, None: No packages downloaded
        return True, string: broken packages info file
        '''
        start = time.time()
        group = os.path.basename(remote)
        remote = '%s/%s' % (setting.URL, remote)
        db_file = os.path.join(local, 'Packages')
        print('==> [%s] Task: Download fresh package database ...' % group)
        if not os.path.exists(local):
            os.makedirs(local)
        for i, db in enumerate(self.db_files, 1):
            url = '%s/%s' % (remote, db)
            out = os.path.join(local, db)
            order = r'%' + str(len(str(len(self.db_files)))) + r's/%s'
            order = order % (i, len(self.db_files))
            result = self._download(url, out, order, db, None, None)
            if result:
                return False, None
        if 'Packages.gz' in self.db_files:
            with gzip.open(os.path.join(local, 'Packages.gz'), 'rb') as dbz:
                data = dbz.read()
                with open(db_file, 'w') as db:
                    db.write(data.decode(encoding='utf-8'))
        if 'Packages.sig' in self.db_files:
            out = os.path.join(local, 'Packages.sig')
            if self._check_sign(out):
                print(' -> %s/Packages signature\033[32m OK\033[0m.' % group)
            else:
                print(' -> %s/Packages signature\033[31m Err\033[0m!' % group)
                return False, None
        if not os.path.exists(db_file):
            print(' -> %s/Packages \033[31m Not Found\033[0m!' % group)
            return False, None
        print(' -> Analyzing %s database ...' % group)
        names = []
        hashs = []
        with open(db_file, 'r') as db:
            data = db.read()
            for match in re.findall(r'Filename: .*\.ipk', data):
                names.append(re.sub(r'Filename: (.*\.ipk)', r'\1', match))
            for match in re.findall(r'%s: .*' % self.db_hash, data):
                hashs.append(re.sub(r'%s: (.*)' % self.db_hash, r'\1', match))
        print(' -> %d packages to download ...' % len(names))
        ask = input('==> [%s] Task: Download packages ... [y/n]?' % group)
        if ask not in ('', 'y', 'Y', 'yes', 'YES'):
            return False, None
        p = Pool(setting.PSIZE)
        order_tmp = r'%' + str(len(str(len(names)))) + r's/%s'
        result = []
        for i, val in enumerate(zip(names, hashs), 1):
            url = '%s/%s' % (remote, val[0])
            out = os.path.join(local, val[0])
            order = order_tmp % (i, len(names))
            result.append(p.apply_async(self._download, args=(
                url, out, order, val[0], self.db_hash_fun, val[1]
            )))
        p.close()
        p.join()
        broken = os.path.join(os.path.dirname(local), group + '-ipks-broken')
        with open(broken, "w") as f:
            for res in result:
                if res.get():
                    f.write('%s -> %s\n' % res.get())
        end = time.time()
        print('==> [%s] Task runs %0.2f seconds.' % (group, (end - start)))
        if not os.path.getsize(broken):
            os.remove(broken)
            return True, ''
        else:
            return True, broken

    def run(self):
        start = time.time()
        broken_list = []
        for c in self.path_couple:
            result, broken = self.download_package_group(*c)
            if result and broken:
                broken_list.append(broken)
        if broken_list:
            print('==> See the broken ipks in:')
            for broken in broken_list:
                print(' -> %s' % broken)
        end = time.time()
        print('==> [ALL] Tasks run %0.2f seconds.' % (end - start))


if __name__ == "__main__":
    g = Grabber(get_profile(setting.PROFILE))
    g.run()
