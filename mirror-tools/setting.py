# -*- coding: utf-8 -*-
# Copyright (C) 2018 shmilee

# 1. set download site, mirror
# URL = 'http://downloads.openwrt.org'
URL = 'http://openwrt.proxy.ustclug.org'

# 2. set processes number, 2-50
PSIZE = 20

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
target_18061_ar71_nand = dict(
    DISTRIB_RELEASE="18.06.1",
    DISTRIB_TARGET="ar71xx/nand",
)
target_snapshot_ar71_nand = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_TARGET="ar71xx/nand",
    IPK_GROUPS=('packages', 'kmods/4.9.123-1-8ee2c7970138017a6e1d590f95efbe9a'),
)

# target: Xiaomi MiWiFi 3G
target_18061_ramips_mt7621 = dict(
    DISTRIB_RELEASE="18.06.1",
    DISTRIB_TARGET="ramips/mt7621",
)
target_snapshot_ramips_mt7621 = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_TARGET="ramips/mt7621",
    IPK_GROUPS=('packages', 'kmods/4.14.66-1-7a4dbe7f80f82ec05db7580bfb4f88f8'),
)

# package: wndr3700v4 etc
package_1806_mips_24kc = dict(
    DISTRIB_RELEASE="18.06",
    DISTRIB_ARCH="mips_24kc",
)
package_snapshot_mips_24kc = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_ARCH="mips_24kc",
)

# package: Xiaomi MiWiFi 3G etc
package_1806_mipsel_24kc = dict(
    DISTRIB_RELEASE="18.06",
    DISTRIB_ARCH="mipsel_24kc",
)
package_snapshot_mipsel_24kc = dict(
    DISTRIB_RELEASE='SNAPSHOT',
    DISTRIB_ARCH="mipsel_24kc",
)

# 6. profile setting
PROFILE = (
    target_18061_ar71_nand
    # target_snapshot_ar71_nand
    # target_18061_ramips_mt7621
    # target_snapshot_ramips_mt7621
    # package_1806_mips_24kc
    # package_snapshot_mips_24kc
    # package_1806_mipsel_24kc
    # package_snapshot_mipsel_24kc
    # etc
)
