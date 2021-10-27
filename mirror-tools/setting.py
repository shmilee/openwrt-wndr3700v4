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
target_21020_ath79_nand = dict(
    DISTRIB_RELEASE="21.02.0",
    DISTRIB_TARGET="ath79/nand",
    IPK_GROUPS=('packages', 'kmods/5.4.143-1-148441b705c0edeb9d20cb5ed52cf971'),
)
target_snapshot_ath79_nand = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_TARGET="ath79/nand",
    IPK_GROUPS=('packages', 'kmods/5.4.152-1-81e0cf03d12565b340efd93ce802a72f'),
)

# package: wndr3700v4 etc
package_2102_mips_24kc = dict(
    DISTRIB_RELEASE="21.02",
    DISTRIB_ARCH="mips_24kc",
)
package_snapshot_mips_24kc = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_ARCH="mips_24kc",
)

# 6. profile setting
PROFILE = (
    target_21020_ath79_nand
    # target_snapshot_ath79_nand
    # package_2102_mips_24kc
    # package_snapshot_mips_24kc
    # etc
)
