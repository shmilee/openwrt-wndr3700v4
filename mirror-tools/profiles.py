# -*- coding: utf-8 -*-

# profile for devices & releases
# Copyright (C) 2016 shmilee

PROFILE_example_release_target = dict(
    # get from /etc/openwrt_release
    DISTRIB_RELEASE="xx.xx",
    DISTRIB_CODENAME="codename",
    DISTRIB_TARGET="cpuarch",
    # packages/group
    # <= 12.09 : None
    # >= 14.07 : ('base', 'luci', 'management', 'packages', 'routing',
    #             'oldpackages', 'telephony')
    IPK_GROUPS=None,
    # packages/database, must contain 'Packages.gz'
    # decompress 'Packages.gz' -> 'Packages'
    # 'md5sums' useless
    # >=15.05 'Packages.gpg', 'Packages.sig'
    DB_FILES=('Packages.gz',),
    # packages Hash Algorithm
    # verify the ipk file
    # 'MD5Sum' or 'SHA256sum'
    DB_HASH='MD5Sum',
)

PROFILES = dict(
    # DB120, 10.03.1 #
    PROFILE_10031_brcm63=dict(
        DISTRIB_RELEASE="10.03.1",
        DISTRIB_CODENAME="backfire",
        DISTRIB_TARGET="brcm63xx",
        IPK_GROUPS=None,
        DB_FILES=('Packages.gz',),
        DB_HASH='MD5Sum',
    ),

    # DB120, 12.09 #
    PROFILE_1209_brcm63=dict(
        DISTRIB_RELEASE="12.09",
        DISTRIB_CODENAME="attitude_adjustment",
        DISTRIB_TARGET="brcm63xx/generic",
        IPK_GROUPS=None,
        DB_FILES=('Packages.gz',),
        DB_HASH='MD5Sum',
    ),

    # DB120, 14.07 #
    PROFILE_1407_brcm63=dict(
        DISTRIB_RELEASE="14.07",
        DISTRIB_CODENAME="barrier_breaker",
        DISTRIB_TARGET="brcm63xx/generic",
        IPK_GROUPS=('base', 'luci', 'management', 'packages', 'routing',
                    'oldpackages',
                    #'telephony' #坑, > 400M
                    ),
        DB_FILES=('Packages.gz', 'md5sums'),
        DB_HASH='MD5Sum',
    ),

    # 3700v4, 14.07 #
    PROFILE_1407_ar71=dict(
        DISTRIB_RELEASE="14.07",
        DISTRIB_CODENAME="barrier_breaker",
        DISTRIB_TARGET="ar71xx/nand",
        IPK_GROUPS=('base', 'luci', 'management', 'packages', 'routing',
                    'oldpackages',
                    #'telephony'
                    ),
        DB_FILES=('Packages.gz', 'md5sums'),
        DB_HASH='SHA256sum',
    ),

    # 3700v4, 15.05.1 #
    PROFILE_15051_ar71=dict(
        DISTRIB_RELEASE="15.05.1",
        DISTRIB_CODENAME="chaos_calmer",
        DISTRIB_TARGET="ar71xx/nand",
        IPK_GROUPS=('base', 'luci', 'management', 'packages', 'routing',
                    #'telephony'
                    ),
        DB_FILES=('Packages.gz', 'Packages.gpg', 'Packages.sig'),
        DB_HASH='SHA256sum',
    ),
)
