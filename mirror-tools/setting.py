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

# set processes number, 2-90
PSIZE = 50
