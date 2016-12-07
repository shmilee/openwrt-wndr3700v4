# -*- coding: utf-8 -*-

from profiles import PROFILES

# set download site, mirror
#URL = 'http://downloads.openwrt.org'
URL = 'http://openwrt.proxy.ustclug.org'

# set prefix for directory to save all the packages
SAVE_PREFIX = './openwrt-ipks-'

# set available PROFILE, see Profiles.py
#PROFILE = 'R10031_brcm63'
#PROFILE = 'R1209_brcm63_generic'
#PROFILE = 'R1407_brcm63_generic'
#PROFILE = 'R1407_ar71_nand'
PROFILE = 'R15051_ar71_nand'
#PROFILE = 'R15051_ar71_generic'
#PROFILE = 'R15051_brcm47_mips74k'
#PROFILE = 'R15051_bcm53_generic'
#PROFILE = 'R15051_ramips_mt7620'
#PROFILE = 'Rtrunk_ramips_mt7628'

# set save directory
SAVEDIR = '%s%s/%s/packages' % (
    SAVE_PREFIX,
    PROFILES[PROFILE]['DISTRIB_RELEASE'],
    PROFILES[PROFILE]['DISTRIB_TARGET']
)

# set processes number, 2-50
PSIZE = 20

# arguments that ``requests.request`` takes
REQUESTS_KWARGS = dict(
    stream=True,
    timeout=min(PSIZE * 3, 90),
    headers={
        'User-Agent': 'Wget/1.17.1 (linux-gnu)'
    },
    proxies={
        #'http': 'http://127.0.0.1:8087',
        #'https': 'http://127.0.0.1:8087',
        #'http': 'socks5://192.168.1.1:3696',
        #'https': 'socks5://192.168.1.1:3696',
    },
)

# check signature of `Packages` by `Packages.sig`
# <15.05, not x86_64, or force to refresh `Packages`
#USIGN_CMD = None
# >=15.05 and x86_64, `usign` from ImageBuilder, `keys` from Images
USIGN_CMD = './db_sign/usign 2>/dev/null -V -P ./db_sign/keys -m'
