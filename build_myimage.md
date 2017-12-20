# 编译 WNDR3700v4 固件

## 准备 Docker image

* 依照 [OpenWrt-build-system-host](./OpenWrt-build-system-host/readme.md) 构建编译环境。

## 准备 ImageBuilder

* 下载 [ImageBuilder](http://openwrt.proxy.ustclug.org/chaos_calmer/15.05.1/ar71xx/nand/OpenWrt-ImageBuilder-15.05.1-ar71xx-nand.Linux-x86_64.tar.bz2)
* 检查MD5: 74af3f78e2d7d4fdc7d65c1ed21a6c78
* 解压 -> `work/ImageBuilder-15.05.1-ar71xx-nand`

## 准备软件源

* 用 mirror-tools 下载官方缓慢的源到本地位置,
  如 `./mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand`.

* 依照 [build_mypackage](./build_mypackage.md) 编译软件包,
  生成的 ipk 放到 `./mypackages`, 然后更新 `package_index`:

  ```
  (cd ./mypackages && \
    ../work/ImageBuilder-15.05.1-ar71xx-nand/scripts/ipkg-make-index.sh . > Packages && \
    gzip -9c Packages > Packages.gz \
  )
  ```

* 修改软件源 `work/ImageBuilder-15.05.1-ar71xx-nand/repositories.conf`.  
  假设 `./mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand` 对应 `/mnt`,  
  `./mypackages` 对应 `/home/openwrt/mypackages` :

```shell
src/gz chaos_calmer_base file:///mnt/packages/base
src/gz chaos_calmer_luci file:///mnt/packages/luci
src/gz chaos_calmer_packages file:///mnt/packages/packages
src/gz chaos_calmer_routing file:///mnt/packages/routing
src/gz chaos_calmer_management file:///mnt/packages/management
src/gz mypackages file:///home/openwrt/mypackages
src imagebuilder file:packages
```

## 准备自定义配置

所有修改过的配置, 按相应路径放入 `./myfiles_templates/`, 这里相当于 `root /`.

**用 `myfiles_secret.py` 保存个人相关信息**, 一个示例 `myfiles_secret-example.py`.

运行 `gen_myfiles.py`, 自动修改 `myfiles_templates/` 生成自定义配置 `myfiles_for_image/`.

```shell
cd ./myfiles_templates/
gpg -d myfiles_secret.py.asc > myfiles_secret.py
./gen_myfiles.py
cd ../
```

## 进入 `Docker container`

```
docker run --rm -i -t -u openwrt \
    -w /home/openwrt/ImageBuilder \
    -v $PWD/work/ImageBuilder-15.05.1-ar71xx-nand:/home/openwrt/ImageBuilder \
    -v $PWD/mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand:/mnt \
    -v $PWD/mypackages:/home/openwrt/mypackages \
    -v $PWD/myfiles_for_image:/home/openwrt/myfiles_for_image \
    shmilee/openwrt-sdk-host:15.05.1 /bin/bash
```

以下命令默认在 `container` 中运行.

## 128M flash

ssh 登录路由查看官方固件的信息:
[1](https://wiki.openwrt.org/doc/techref/flash.layout)

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

ubi firmware 组合:

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

修改 `/home/openwrt/ImageBuilder/target/linux/ar71xx/image/Makefile`.
找到以 `wndr4300_mtdlayout` 开头的行, 尽量多的使用 128M nand flash.

```shell
$ ubi=110592 #108M
$ firmware=112640 #110M
$ cd /home/openwrt/ImageBuilder/target/linux/ar71xx/image
$ cp Makefile Makefile.bk
$ sed -i "s/\(^wndr4300_mtdlayout.*\)23552k\(.ubi..\)25600k\(.*$\)/\1${ubi}k\2${firmware}k\3/" Makefile
$ diff -u0 Makefile.bk Makefile
--- Makefile.bk	2017-12-18 05:25:16.000000000 +0000
+++ Makefile	2017-12-18 05:25:26.000000000 +0000
@@ -1010 +1010 @@
-wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),23552k(ubi),25600k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
+wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),110592k(ubi),112640k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
```

## PROFILE

查看支持的 Profiles. NETGEAR WNDR3700v4/WNDR430 共用一个 Profile.

```shell
$ cd /home/openwrt/ImageBuilder/
$ make info
Current Target: "ar71xx (Generic devices with NAND flash)"
Default Packages: base-files libc libgcc busybox dropbear mtd uci opkg
netifd fstools kmod-gpio-button-hotplug swconfig kmod-ath9k wpad-mini
uboot-envtools dnsmasq iptables ip6tables ppp ppp-mod-pppoe
kmod-nf-nathelper firewall odhcpd odhcp6c

WNDR4300:
	NETGEAR WNDR3700v4/WNDR4300
	Packages: kmod-usb-core kmod-usb-ohci kmod-usb2 kmod-ledtrig-usbdev
```

## PACKAGES

检查默认的 Packages, 删除或添加软件源中的 Packages.

```shell
replace_ipks=(
    -dnsmasq
    dnsmasq-full
)
luci_ipks=(
    luci luci-i18n-base-zh-cn luci-i18n-firewall-zh-cn
    luci-app-ddns luci-i18n-ddns-zh-cn
    #luci-app-minidlna luci-i18n-minidlna-zh-cn
    #luci-app-privoxy luci-i18n-privoxy-zh-cn
    luci-app-qos luci-i18n-qos-zh-cn
    luci-app-samba luci-i18n-samba-zh-cn
    luci-app-sqm
    luci-app-statistics luci-i18n-statistics-zh-cn
    #luci-app-tinyproxy  luci-i18n-tinyproxy-zh-cn
    luci-app-transmission luci-i18n-transmission-zh-cn
    #luci-app-upnp luci-i18n-upnp-zh-cn
    luci-app-watchcat luci-i18n-watchcat-zh-cn
    luci-app-wol luci-i18n-wol-zh-cn
    )
zjuvpn_ipks=(
    kmod-l2tp
    kmod-pppol2tp
    ppp-mod-pppol2tp
    xl2tpd
    )
other_ipks=(
    ca-certificates # for aria2 verify https
    htop
    iftop
    ip
    openssh-client
    #sshfs
    shadow-su
    shadow-useradd
    ss
    nfs-kernel-server-utils # cmd: nfsstat showmount
    )
```

添加 USB 存储。

> 关于 [block-mount](https://wiki.openwrt.org/doc/techref/block_mount)

> `block-mount_2016-01-10-96415af` `block info` 可以检测到的[文件系统](http://git.openwrt.org/?p=project/fstools.git;a=tree;f=libblkid-tiny;h=ccdd3a9887552b83cc2e1749bea25356ad78fe0a;hb=96415afecef35766332067f4205ef3b2c7561d21)

```shell
usb_ipks=(
    kmod-usb-core kmod-usb2 kmod-usb-ohci
    kmod-usb-storage
    kmod-usb-storage-extras
    mount-utils
    block-mount
    kmod-fs-ext4
    # btrfs 据说分区损坏不易恢复
    #kmod-fs-btrfs
    # FAT32 4GB file size limitation
    #kmod-fs-vfat
    # `block info` cannot detect reiserfs, ntfs
    #kmod-fs-reiserfs kmod-fs-ntfs ntfs-3g
    luci-app-hd-idle luci-i18n-hd-idle-zh-cn
    )
```

添加自己编译的 mypackages.

```shell
my_ipks=(
    autossh luci-app-autossh luci-i18n-autossh-zh-cn
    nginx
    aria2 luci-app-aria2 luci-i18n-aria2-zh-cn
    ariang
    #yaaw
    vlmcsd luci-app-vlmcsd
    miredo-client miredo-server
    shadowsocks-libev luci-app-shadowsocks
    adbyby luci-app-adbyby-plus luci-i18n-adbyby-plus-zh-cn
    goagent-client
    #frpc frps
    luci-app-nfs luci-i18n-nfs-zh-cn
)
```


## 编译

```shell
$ cd /home/openwrt/ImageBuilder/
$ make image \
  PROFILE=WNDR4300 \
  PACKAGES="$(echo\
    ${replace_ipks[@]}\
    ${luci_ipks[@]}\
    ${zjuvpn_ipks[@]}\
    ${usb_ipks[@]}\
    ${other_ipks[@]}\
    ${my_ipks[@]})" \
  FILES="/home/openwrt/myfiles_for_image"
```

生成的镜像位置 `/home/openwrt/ImageBuilder/bin/ar71xx/`,
文件名 `openwrt-15.05.1-ar71xx-nand-wndr3700v4-ubi-factory.img`.
