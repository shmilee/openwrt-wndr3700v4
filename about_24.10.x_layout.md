

# 128M flash layout of WNDR3700v4 24.10.x

1. flash layout 相关的一些参考链接：
    - openwrt [flash layout 的介绍文档](https://openwrt.org/docs/techref/flash.layout)
    - [dts 设备树介绍](https://cloud.tencent.com/developer/article/2008640)
    - https://blog.csdn.net/u011570312/article/details/112269634
    - https://www.red-yellow.net/netgear-wndr3700-v4刷openwrt固件.html
    - 用于 NAND flash 的 [UBIFS（无序区块镜像文件系统）](https://en.wikipedia.org/wiki/UBIFS)

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
        + 第二部分 `/dev/ubi0_1` 用于 `/overlay`。  
        + 89684 "ubiconcat1"(mtd11,96M)
         对应 `ubiconcat0`
         对应 `ubiconcat1`


Filesystem           1K-blocks      Used Available Use% Mounted on
/dev/ubi0_1              89684        72     84992   0% /overlay
overlayfs:/overlay       89684        72     84992   0% /

/dev/ubi0_1 on /overlay type ubifs (rw,noatime,assert=read-only,ubi=0,vol=1)


```
```




仅当编译的固件体积过大时，才需要考虑修改 layout。
比如，固件中加入了go编译的较大软件包，才需重点检查 kernel+firmware 的体积。




3. 修改 layout 的相关文件。

* `target/linux/ath79/dts/ar9344_netgear_wndr.dtsi`


