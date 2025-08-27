# 128M flash layout of WNDR3700v4 19.07.x

## 登录路由查看

```shell
## firmware = kernel + ubi, kernel is 2048k
$ cat /proc/cmdline 
 board=WNDR3700_V4 console=ttyS0,115200 mtdparts=ar934x-nfc:256k(u-boot)ro,
256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),
3072k(traffic_meter),2048k(kernel),23552k(ubi),25600k@0x6c0000(firmware),
256k(caldata_backup),-(reserved) rootfstype=squashfs noinitrd

$ cat /proc/mtd
dev:    size   erasesize  name
mtd0: 00040000 00020000 "u-boot"
mtd1: 00040000 00020000 "u-boot-env"
mtd2: 00040000 00020000 "caldata"
mtd3: 00080000 00020000 "pot"
mtd4: 00200000 00020000 "language"
mtd5: 00080000 00020000 "config"
mtd6: 00300000 00020000 "traffic_meter"
mtd7: 00200000 00020000 "kernel"
mtd8: 01700000 00020000 "ubi"
mtd9: 01900000 00020000 "firmware"
mtd10: 00040000 00020000 "caldata_backup"
mtd11: 06000000 00020000 "reserved"

$ cat /proc/partitions 
major minor  #blocks  name

  31        0        256 mtdblock0
  31        1        256 mtdblock1
  31        2        256 mtdblock2
  31        3        512 mtdblock3
  31        4       2048 mtdblock4
  31        5        512 mtdblock5
  31        6       3072 mtdblock6
  31        7       2048 mtdblock7
  31        8      23552 mtdblock8
  31        9      25600 mtdblock9
  31       10        256 mtdblock10
  31       11      98304 mtdblock11
 254        0       2356 ubiblock0_0
## sum(name[0,1,2,3,4,5,6,10]) = 7M
## name7 + name8 = name9
## name11 (reserved)
## name9 + name 11 = 123904(121M) -> firmware, 123904 - name7 = 121856 -> ubi
```

## ubi firmware 组合

```
ubi=23552 #23M
firmware=25600 #25M

ubi=49152 #48M
firmware=51200 #50M

ubi=74752 #73M
firmware=76800 #75M

ubi=100352 #98M
firmware=102400 #100M

ubi=110592 #108M
firmware=112640 #110M

ubi=121856 #119M
firmware=123904 #121M, 最大值
```

## 修改 `/home/openwrt/imagebuilder/target/linux/ath79/image/legacy.mk`

找到以 `wndr4300_mtdlayout` 开头的行, 尽量多的使用 128M nand flash.

```shell
$ ubi=110592 #108M
$ firmware=112640 #110M
$ cd /home/openwrt/imagebuilder/target/linux/ar71/image
$ cp legacy.mk legacy.mk.bk
$ sed -i "s/\(^wndr4300_mtdlayout.*\)23552k\(.ubi..\)25600k\(.*$\)/\1${ubi}k\2${firmware}k\3/" legacy.mk
$ diff -u0 legacy.mk.bk legacy.mk
--- legacy.mk.bk	2018-08-28 12:04:14.000000000 +0000
+++ legacy.mk	2018-08-28 12:04:21.000000000 +0000
@@ -273 +273 @@
-wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),23552k(ubi),25600k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
+wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),110592k(ubi),112640k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
```

