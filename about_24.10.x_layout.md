---
title: flash layout of WNDR3700v4
subtitle: for openwrt 24.10.x
author:
    - shmilee
date: \today
CJKmainfont: SimSun
fontsize: 10pt  # 8pt, 10pt, 12pt, 14pt
---

# 128M flash layout of WNDR3700v4 24.10.x

1. flash layout 相关的一些参考链接：
    - openwrt [flash layout 的介绍文档](https://openwrt.org/docs/techref/flash.layout)
    - https://www.red-yellow.net/netgear-wndr3700-v4刷openwrt固件.html
    - https://blog.csdn.net/u011570312/article/details/112269634
    - 用于 NAND flash 的 [UBIFS（无序区块镜像文件系统）](https://en.wikipedia.org/wiki/UBIFS)
    - [DTS 设备树介绍](https://cloud.tencent.com/developer/article/2008640)
    - [kernel DTS coding style](https://docs.kernel.org/devicetree/bindings/dts-coding-style.html)

2. 刷使用默认分区布局的固件（官方或自建）。ssh 登录路由，查看固件信息。  
  mtd size 十六进制，单位 B。partitions blocks 十进制，单位 KB。

```
root@OpenWrt:~# cat /proc/mtd
dev:    size   erasesize  name
mtd0: 00040000 00020000 "u-boot"
mtd1: 00040000 00020000 "u-boot-env"
mtd2: 00040000 00020000 "caldata"
mtd3: 00080000 00020000 "pot"
mtd4: 00200000 00020000 "language"
mtd5: 00080000 00020000 "config"
mtd6: 00300000 00020000 "traffic_meter"
mtd7: 01900000 00020000 "firmware"
mtd8: 00400000 00020000 "kernel"
mtd9: 01500000 00020000 "ubiconcat0"
mtd10: 00040000 00020000 "caldata_backup"
mtd11: 06000000 00020000 "ubiconcat1"
mtd12: 07500000 00020000 "ubi"

root@OpenWrt:~# cat /proc/partitions
major minor  #blocks  name

  31        0        256 mtdblock0
  31        1        256 mtdblock1
  31        2        256 mtdblock2
  31        3        512 mtdblock3
  31        4       2048 mtdblock4
  31        5        512 mtdblock5
  31        6       3072 mtdblock6
  31        7      25600 mtdblock7
  31        8       4096 mtdblock8
  31        9      21504 mtdblock9
  31       10        256 mtdblock10
  31       11      98304 mtdblock11
  31       12     119808 mtdblock12
 254        0      14012 ubiblock0_0

root@OpenWrt:~# df
Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/root                14080     14080         0 100% /rom
tmpfs                    60112       748     59364   1% /tmp
/dev/ubi0_1              89684        72     84992   0% /overlay
overlayfs:/overlay       89684        72     84992   0% /
tmpfs                      512         0       512   0% /dev

root@OpenWrt:~# ls /dev/ubi*
/dev/ubi0         /dev/ubi0_0       /dev/ubi0_1       /dev/ubi_ctrl     /dev/ubiblock0_0

root@OpenWrt:~# mount|grep /dev
/dev/ubiblock0_0 on /rom type squashfs (ro,relatime,errors=continue)
/dev/ubi0_1 on /overlay type ubifs (rw,noatime,assert=read-only,ubi=0,vol=1)
tmpfs on /dev type tmpfs (rw,nosuid,noexec,noatime,size=512k,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,noatime,mode=600,ptmxmode=000)

root@OpenWrt:~# ubinfo
UBI version:                    1
Count of UBI devices:           1
UBI control device major/minor: 10:127
Present UBI devices:            ubi0

root@OpenWrt:~# ubinfo /dev/ubi0
ubi0
Volumes count:                           2
Logical eraseblock size:                 126976 bytes, 124.0 KiB
Total amount of logical eraseblocks:     936 (118849536 bytes, 113.3 MiB)
Amount of available logical eraseblocks: 0 (0 bytes)
Maximum count of volumes                 128
Count of bad physical eraseblocks:       0
Count of reserved physical eraseblocks:  19
Current maximum erase counter value:     2
Minimum input/output unit size:          2048 bytes
Character device major/minor:            249:0
Present volumes:                         0, 1

root@OpenWrt:~# ubinfo /dev/ubi0_0
Volume ID:   0 (on ubi0)
Type:        dynamic
Alignment:   1
Size:        113 LEBs (14348288 bytes, 13.6 MiB)
State:       OK
Name:        rootfs
Character device major/minor: 249:1

root@OpenWrt:~# ubinfo /dev/ubi0_1
Volume ID:   1 (on ubi0)
Type:        dynamic
Alignment:   1
Size:        800 LEBs (101580800 bytes, 96.8 MiB)
State:       OK
Name:        rootfs_data
Character device major/minor: 249:2
```

* 在目录 `./work/imagebuilder-24.10.2-ath79-nand/` 内，寻找layout相关文件。
    - `make info` 输出 -> `netgear_wndr3700-v4`.
    - `Device/netgear_wndr3700-v4` defined in **`target/linux/ath79/image/nand.mk`**, uses `Device/netgear_ath79_nand`.
    - `Device/netgear_ath79_nand` defined in **`target/linux/ath79/image/nand.mk`**.
        + `KERNEL_SIZE := 4096k`，4M，对应于
            ```
            mtd8: 00400000 00020000 "kernel"
            31        8       4096 mtdblock8
            ```
        + `BLOCKSIZE := 128k`，最小块大小
        + `IMAGE_SIZE := 25600k`，25M，对应于
            ```
            mtd7: 01900000 00020000 "firmware"
            31        7      25600 mtdblock7
            ```
    - 3700-v4 的 dts 文件，`find target/|grep 3700-v4` 输出 **`target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts`**
    - `#include ar9344_netgear_wndr.dtsi`，即 **`target/linux/ath79/dts/ar9344_netgear_wndr.dtsi`**
    - `&nand` -> `partitions` 设置了各分区位置和长度等属性。
        + reg 属性值，包括**起始地址**和**地址长度**(十六进制)。
        + #address-cells, #size-cells, reg 地址字、长度段占用几个 u32
    - `/` -> `ubi-concat` **合并**有间隔的分区 `ubiconcat0` 和 `ubiconcat1` 为 `ubi@0`。
      其中 `ubiconcat1` 对应旧版 19.07.x 未利用的部分。
      因此 24.10.2 已充分利用了 128M 的闪存。

* 根据 `ar9344_netgear_wndr.dtsi` 给出默认的 flash layout。可对照 `/proc/mtd` 和 `/proc/partitions`。
    - u-boot和其他前7个分区：  
        + 启动相关的 "u-boot"(mtd0,256k)、"u-boot-env"(mtd1,256k)，  
        + "caldata"(mtd2,256k)、"pot"(mtd3,512k)、"language"(mtd4,2M)
        + "config"(mtd5,512k)、"traffic\_meter"(mtd6,3M)
        + mtd0 到 mtd6 的地址和长度：<0x0 0x6c0000>，
          共 `256k+256k + 256k+512k + 2M + 512k + 3M = 6.75M`
    - 固件 "firmware"(mtd7,25M) = "kernel"(mtd8,4M) + "ubiconcat0"(mtd9,21M)
        + mtd7 的地址和长度：<0x6c0000 0x1900000>
    - "caldata\_backup"(mtd10,256k)
        + mtd10 的地址和长度：<0x1fc0000 0x40000>
    - "ubiconcat1"(mtd11,96M)
        + mtd11 的地址和长度：<0x2000000 0x6000000>
    - UBI partition：由 "ubiconcat0"(mtd9) 和 "ubiconcat1"(mtd11) 两部分组成。
        + "ubi"(mtd12,117M) = (mtd9,21M) + (mtd11,96M)
        + 相比于 19.07.x 最大"ubi"(119M)，减小的 2M 给了 kernel（2M -> 4M）。
    - 挂载的文件系统中 ubi （即 `/dev/ubi0`，dtsi 中的 `ubi@0`）的利用情况：
        + 第一部分 `/dev/ubi0_0` 用于固件中的 rootfs。  
          rootfs 挂载为 `/rom`, uses SquashFS, 大小取决于包含的软件包多少。  
          上文 `14012 ubiblock0_0` 对应 `14080k /rom`，固件中 /rom 略大，因为其最小块 `BLOCKSIZE:=128k`。
        + 第二部分 `/dev/ubi0_1`, uses ubifs, 用于 `/overlay`。  
          可用大小 89684k 少于 "ubiconcat1"(mtd11,96M)。
          ubi 的两个 volume 卷均小于两个分区 `ubiconcat0` 和 `ubiconcat1` 的最大可用值。

```
+-----------+-------------------------------------------------------------------------------------------------+
|  Layer-0  |                                            raw flash                                            |
+===========+=================+=================================+=====================+=======================+
| Layer-1.1 | u-boot & other, |            firmware,            |   caldata_backup,   |      ubiconcat1,      |
|           |  <0x0 0x6c0000> |       <0x6c0000 0x1900000>      | <0x1fc0000 0x40000> | <0x2000000 0x6000000> |
|           |   mtd0 to mtd6  |           mtd7, (25M)           |        mtd10        |      mtd11, (96M)     |
+-----------+-----------------+------------+--------------------+---------------------+                       |
| Layer-1.2 |                 |   kernel   |     ubiconcat0     |          X          |                       |
|           |                 | mtd8, (4M) |     mtd9, (21M)    |                     |                       |
+-----------+-----------------+------------+--------------------+---------------------+-----------------------+
| Layer-1.3 |                 |            |              UBI partition, mtd12=mtd9+mtd11, (117M)             |
+-----------+-----------------+------------+--------------------+---------------------------------------------+
|  Layer-2  |                 |            |       rootfs,      |                 rootfs_data,                |
|           |                 |            |  dynamic volume 0, |              dynamic volume 1,              |
|           |                 |            |  mounted: "/rom",  |             mounted: "/overlay",            |
|           |                 |            |      SquashFS,     |                    UBIFS,                   |
|           |                 |            |   size depends on  |           all remaining free space          |
|           |                 |            |    selected pkgs   |                                             |
+-----------+-----------------+------------+--------------------+---------------------------------------------+
|  Layer-3  |                 |            |     mounted: "/", OverlayFS, stacking /overlay on top of /rom    |
+-----------+-----------------+------------+------------------------------------------------------------------+
```

3. 仅当编译的固件体积过大时，才需要考虑修改 layout。
   比如，固件中加入了go编译的较大软件包，才需重点检查 kernel+rootfs，即 firmware 的体积。

   在下载和构建固件的网站：[firmware-selector.openwrt.org](https://firmware-selector.openwrt.org/?version=24.10.2&target=ath79%2Fnand&id=netgear_wndr3700-v4)，
   添加预安装的软件包 `tailscale adguardhome v2raya`，构建过程出现如下错误：
   ```
   WARNING: Image file /builder/build_dir/target-mips_24kc_musl/linux-ath79_nand/tmp/openwrt-24.10.2-5f203f8f3f51-ath79-nand-netgear_wndr3700-v4-squashfs-factory.img
   is too big: 39714816 > 26214400
   [mkdniimg] *** error: stat failed on /builder/build_dir/target-mips_24kc_musl/linux-ath79_nand/tmp/openwrt-24.10.2-5f203f8f3f51-ath79-nand-netgear_wndr3700-v4-squashfs-factory.img: No such file or directory
   make[3]: *** [Makefile:125: /builder/build_dir/target-mips_24kc_musl/linux-ath79_nand/tmp/openwrt-24.10.2-5f203f8f3f51-ath79-nand-netgear_wndr3700-v4-squashfs-factory.img] Error 1
   make[2]: *** [Makefile:268: build_image] Error 2
   ```
   其中，
   ```
   [rootfs]
   mode=ubi
   vol_id=0
   vol_type=dynamic
   vol_name=rootfs
   image=/builder/build_dir/target-mips_24kc_musl/linux-ath79_nand/root.squashfs
   vol_size=33451008
   ```

4. 根据 rootfs 的 `vol_size` 或 `IMAGE_SIZE = 39714816 > 25M`，修改 layout 的相关文件。
   
* `target/linux/ath79/image/nand.mk`, add `CUSTOM_IMAGE_SIZE=??m` support

```patch
@@ -366,6 +366,9 @@
 endef
 TARGET_DEVICES += netgear_r6100
 
+# add cuttom wndr3700-v4 setting
+#   IMAGE_SIZE reset, $$() -> $() when using
+#   DTS_CPPFLAGS, for #if #include in dtsi, not checked/used
 define Device/netgear_wndr3700-v4
   SOC := ar9344
   DEVICE_MODEL := WNDR3700
@@ -374,6 +377,8 @@
   NETGEAR_BOARD_ID := WNDR3700v4
   NETGEAR_HW_ID := 29763948+128+128
   $(Device/netgear_ath79_nand)
+  IMAGE_SIZE := $$(if $$(CUSTOM_IMAGE_SIZE),$$(CUSTOM_IMAGE_SIZE),25600k)
+  DTS_CPPFLAGS := $$(if $$(CUSTOM_IMAGE_SIZE),-D__CUSTOM_IMAGE_SIZE__)
 endef
 TARGET_DEVICES += netgear_wndr3700-v4
```

* `target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts` -/> `target/linux/ath79/dts/ar9344_netgear_wndr.dtsi`

```patch
@@ -1,6 +1,6 @@
 // SPDX-License-Identifier: GPL-2.0-or-later OR MIT
 
-#include "ar9344_netgear_wndr.dtsi"
+#include "ar9344_netgear_wndr_custom_image_size.dtsi"
 #include "ar9344_netgear_wndr_wan.dtsi"
 #include "ar9344_netgear_wndr_usb.dtsi"
 ```

* Create file `ar9344_netgear_wndr_custom_image_size.dtsi`
  by script `target-linux-ath79-dts-ar9344_netgear_wndr_custom_image_size.py`.

commands example for `CUSTOM_IMAGE_SIZE=40m`:

```
patch -i ./flash-layout/ath79-image-nand.mk.patch ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk
patch -i ./flash-layout/ath79-dts-ar9344_netgear_wndr3700-v4.dts.patch ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts
./flash-layout/ath79-dts-ar9344_netgear_wndr_custom_image_size.py --imgsize 40m ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/dts/ar9344_netgear_wndr.dtsi
```
