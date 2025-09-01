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

3. 在目录 `./work/imagebuilder-24.10.2-ath79-nand/`（或 `./work/sdk-24.10.2-ath79-nand/`）内，寻找layout相关文件。
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

4. 根据 `ar9344_netgear_wndr.dtsi` 给出默认的 flash layout。可对照 `/proc/mtd` 和 `/proc/partitions`。
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

# 修改 flash layout of WNDR3700v4

1. 仅当编译的固件体积过大时，才需要考虑修改 layout。
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

2. 根据 rootfs 的 `vol_size` 或 `IMAGE_SIZE = 39714816 > 25M`，修改 layout 的相关文件。
   
* `target/linux/ath79/image/nand.mk`, add `CUSTOM_IMAGE_SIZE=??m` support
    - change `IMAGE_SIZE`
    - add `DEVICE_DTS=ar9344_netgear_wndr3700-v4-custom-$(CUSTOM_IMAGE_SIZE)`,
      see `Device/Build/kernel` in `include/image.mk`
    - add `DTS_CPPFLAGS`, see `Image/BuildDTB/sub` in `include/image.mk`
    - patch: `./flash-layout/ath79-image-nand.mk.patch`

* Create file `target/linux/ath79/dts/ar9344_netgear_wndr3700-v4-custom-??m.dts`
  by script `ar9344_netgear_wndr3700-v4-custom-image_size.py`.


3. imagebuilder 内测试，修改的 dts 未生效。

commands example for `CUSTOM_IMAGE_SIZE=40m`:

```
patch -i ./flash-layout/ath79-image-nand.mk.patch ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk
./flash-layout/ar9344_netgear_wndr3700-v4-custom-image_size.py --imgsize 40m \
    ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts
## then run in imagebuilder container
make image ADD_LOCAL_KEY=1 PROFILE=netgear_wndr3700-v4 CUSTOM_IMAGE_SIZE=40m
```

修改不生效，因为
* imagebuilder 生成固件时，目录 `build_dir/target-mips_24kc_musl/linux-ath79_nand/` 内，
    - 不更新 `netgear_wndr3700-v4-kernel.bin`，
    - 无需生成新的 `image-ar9344_netgear_wndr3700-v4-custom-40m.dtb`，
    - 所以修改不生效，ubiconcat0 仍是 21M。
    - 参考：[How OpenWrt compiles DTS files?](https://forum.openwrt.org/t/how-openwrt-compiles-dts-files/67532)
* 一个 mtd 分区可有多个 ubi volume，但一个 ubi volume 不能横跨多个 mtd 分区。
    - 参考：[NAND/MTD/UBI/UBIFS 概念及使用方法](https://www.cnblogs.com/arnoldlu/p/17689046.html)
    - 因此大于 21M 的 /rom rootfs 无法放入 ubiconcat0，刷机失败。

4. 结合 `imagebuilder-24.10.2-ath79-nand` 和 `sdk-24.10.2-ath79-nand` 生成 `dtb` 并 更新 `kernel.bin`。
    - 参考：[Custom DTS / DTB building with ImageBuilder](https://lists.openwrt.org/pipermail/openwrt-devel/2021-March/034239.html)

```
cp -v ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk{,.backup~}
patch -i ./flash-layout/ath79-image-nand.mk.patch ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk
cp -v ./work/sdk-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk{,.backup~}
patch -i ./flash-layout/ath79-image-nand.mk.patch ./work/sdk-24.10.2-ath79-nand/target/linux/ath79/image/nand.mk

./flash-layout/ar9344_netgear_wndr3700-v4-custom-image_size.py --imgsize 40m \
    ./work/imagebuilder-24.10.2-ath79-nand/target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts
./flash-layout/ar9344_netgear_wndr3700-v4-custom-image_size.py --imgsize 40m \
    ./work/sdk-24.10.2-ath79-nand/target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts

docker run --rm -i -t -u openwrt \
    -w /home/openwrt \
    -v $PWD/work/sdk-24.10.2-ath79-nand:/home/openwrt/sdk \
    -v $PWD/work/imagebuilder-24.10.2-ath79-nand:/home/openwrt/imagebuilder \
    shmilee/openwrt-buildsystem:24.10.x /bin/bash
```

在容器内：
    - vmlinux 不重新编译，copy imagebuilder to sdk 即可
    - PATH 无需 cpp 的 `staging_dir/toolchain-mips_24kc_gcc-13.3.0_musl/bin`
    - 无需指定 `TARGET_BUILD=1 BOARD="ath79" DEVICE_DTS=ar9344_netgear_wndr3700-v4-custom-xx`

```
dtb_kernel_DIR='build_dir/target-mips_24kc_musl/linux-ath79_nand'

vmlinux_bin="$dtb_kernel_DIR/vmlinux"
cp -iv ~/imagebuilder/$vmlinux_bin ~/sdk/$vmlinux_bin

cd ~/sdk/
kernel_bin="$dtb_kernel_DIR/netgear_wndr3700-v4-kernel.bin"
PATH="$HOME/sdk/staging_dir/host/bin:$PATH" make --trace \
    -C target/linux/ath79/image "$HOME/sdk/$kernel_bin" \
    TOPDIR="$HOME/sdk" INCLUDE_DIR="$HOME/sdk/include" SUBTARGET="nand" \
    PROFILE=netgear_wndr3700-v4 CUSTOM_IMAGE_SIZE=40m

## check
ls -lh ~/sdk/$dtb_kernel_DIR/*3700*
md5sum ~/sdk/$dtb_kernel_DIR/*3700*

## backup
mkdir -v ~/imagebuilder/$dtb_kernel_DIR/netgear_wndr3700-v4-orignal-25m
mv -v ~/imagebuilder/$dtb_kernel_DIR/*3700* ~/imagebuilder/$dtb_kernel_DIR/netgear_wndr3700-v4-orignal-25m

## cp
cp -iv ~/sdk/$dtb_kernel_DIR/*3700* ~/imagebuilder/$dtb_kernel_DIR/

## 构建固件，docker run with local packages dir mounted
##cd ~/imagebuilder/
##make image ADD_LOCAL_KEY=1 PROFILE=netgear_wndr3700-v4 CUSTOM_IMAGE_SIZE=40m
```
