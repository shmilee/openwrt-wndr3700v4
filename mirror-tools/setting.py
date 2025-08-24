# -*- coding: utf-8 -*-
# Copyright (C) 2018 shmilee

# 1. set download site, mirror
# URL = 'http://downloads.openwrt.org'
URL = 'https://openwrt.proxy.ustclug.org'

# 2. set processes number, 2-50
PSIZE = 10

# 3. arguments that ``requests.request`` takes
REQUESTS_KWARGS = dict(
    stream=True,
    timeout=min(PSIZE * 3, 90),
    headers={
        'User-Agent': 'Wget/1.17.1 (linux-gnu)'
    },
    proxies={
        # 'http': 'http://127.0.0.1:8087',
        # 'https': 'http://127.0.0.1:8087',
        # 'http': 'socks5://192.168.1.1:3696',
        # 'https': 'socks5://192.168.1.1:3696',
    },
)

# 4. check signature of `Packages`, need `Packages.sig`
# <15.05, not x86_64
# USIGN_CMD = None
# >=15.05 and x86_64, `usign` from ImageBuilder, `keys` from Images
USIGN_CMD = './db_sign/usign 2>/dev/null -V -P ./db_sign/keys -m'

# 5. Profiles lib
# target: wndr3700v4
target_24102_ath79_nand = dict(
    DISTRIB_RELEASE="24.10.2",
    DISTRIB_TARGET="ath79/nand",
    IPK_GROUPS=('packages', 'kmods/6.6.93-1-ba16238a7a163b7e7c5402245d60bef1'),
)
target_snapshot_ath79_nand = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_TARGET="ath79/nand",
    IPK_GROUPS=('packages', 'kmods/6.12.40-1-610eee3372c3c0c9aa70715350022b98'),
)

# package: wndr3700v4 etc
package_2410_mips_24kc = dict(
    DISTRIB_RELEASE="24.10",
    DISTRIB_ARCH="mips_24kc",
)
package_snapshot_mips_24kc = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_ARCH="mips_24kc",
)

# 6. profile setting
PROFILE = (
    target_24102_ath79_nand
    # target_snapshot_ath79_nand
    # package_2410_mips_24kc
    # package_snapshot_mips_24kc
    # etc
)
