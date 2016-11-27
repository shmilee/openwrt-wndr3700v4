# -*- coding: utf-8 -*-

from profiles import PROFILES

# set download site, mirror
#URL = 'http://downloads.openwrt.org'
URL = 'http://openwrt.proxy.ustclug.org'

# set prefix for directory to save all the packages
SAVE_PREFIX = './openwrt-ipks-'

# set available PROFILE, see Profiles.py
#PROFILE = 'PROFILE_10031_brcm63'
#PROFILE = 'PROFILE_1209_brcm63'
#PROFILE = 'PROFILE_1407_brcm63'
#PROFILE = 'PROFILE_1407_ar71'
PROFILE = 'PROFILE_15051_ar71'

# set save directory
SAVEDIR = '%s%s/%s/packages' % (
    SAVE_PREFIX,
    PROFILES[PROFILE]['DISTRIB_RELEASE'],
    PROFILES[PROFILE]['DISTRIB_TARGET']
)

# set processes number, 2-90
PSIZE = 50
