# 编译 WNDR3700v4 固件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

## 准备 ImageBuilder

* 下载 [ImageBuilder](http://openwrt.proxy.ustclug.org/releases/18.06.1/targets/ar71xx/nand/openwrt-imagebuilder-18.06.1-ar71xx-nand.Linux-x86_64.tar.xz)
* 检查MD5, 解压 -> `work/imagebuilder-18.06.1-ar71xx-nand`

## 准备软件源

* 用 mirror-tools 下载官方缓慢的源到本地位置,
  如 `./mirror-tools/{openwrt-18.06.1,openwrt-packages-18.06}`.

* 依照 [build_mypackage](./build_mypackage.md) 编译软件包,
  生成的 ipk, `package_index` 放到 `./mypackages`

* 修改软件源 `work/imagebuilder-18.06.1-ar71xx-nand/repositories.conf`.  
  假设 `./mirror-tools` 对应 `/mnt`,  
  `./mypackages` 对应 `/home/openwrt/mypackages` :

```shell
src/gz openwrt_core file:///mnt/openwrt-18.06.1/targets/ar71xx/nand/packages
src/gz openwrt_base file:///mnt/openwrt-packages-18.06/mips_24kc/base
src/gz openwrt_luci file:///mnt/openwrt-packages-18.06/mips_24kc/luci
src/gz openwrt_packages file:///mnt/openwrt-packages-18.06/mips_24kc/packages
src/gz openwrt_routing file:///mnt/openwrt-packages-18.06/mips_24kc/routing
src/gz openwrt_telephony file:///mnt/openwrt-packages-18.06/mips_24kc/telephony
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
    -w /home/openwrt/imagebuilder \
    -v $PWD/work/imagebuilder-18.06.1-ar71xx-nand:/home/openwrt/imagebuilder \
    -v $PWD/mirror-tools:/mnt \
    -v $PWD/mypackages:/home/openwrt/mypackages \
    -v $PWD/myfiles_for_image:/home/openwrt/myfiles_for_image \
    shmilee/openwrt-buildsystem:18.06.1 /bin/bash
```

以下命令默认在 `container` 中运行.

## 128M flash

ssh 登录路由查看官方固件的信息:
[1](https://openwrt.org/docs/techref/flash.layout)

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

修改 `/home/openwrt/imagebuilder/target/linux/ar71xx/image/legacy.mk`.
找到以 `wndr4300_mtdlayout` 开头的行, 尽量多的使用 128M nand flash.

```shell
$ ubi=110592 #108M
$ firmware=112640 #110M
$ cd /home/openwrt/imagebuilder/target/linux/ar71xx/image
$ cp legacy.mk legacy.mk.bk
$ sed -i "s/\(^wndr4300_mtdlayout.*\)23552k\(.ubi..\)25600k\(.*$\)/\1${ubi}k\2${firmware}k\3/" legacy.mk
$ diff -u0 legacy.mk.bk legacy.mk
--- legacy.mk.bk	2018-08-28 12:04:14.000000000 +0000
+++ legacy.mk	2018-08-28 12:04:21.000000000 +0000
@@ -273 +273 @@
-wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),23552k(ubi),25600k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
+wndr4300_mtdlayout=mtdparts=ar934x-nfc:256k(u-boot)ro,256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),3072k(traffic_meter),2048k(kernel),110592k(ubi),112640k@0x6c0000(firmware),256k(caldata_backup),-(reserved)
```

## PROFILE

查看 Profile `NETGEAR WNDR3700v4`.

```shell
$ cd /home/openwrt/imagebuilder/
$ make info
Current Target: "ar71xx (Generic devices with NAND flash)"
Default Packages: base-files libc libgcc busybox dropbear mtd uci opkg
netifd fstools uclient-fetch logd kmod-gpio-button-hotplug swconfig
kmod-ath9k wpad-mini uboot-envtools dnsmasq iptables ip6tables
ppp ppp-mod-pppoe firewall odhcpd-ipv6only odhcp6c

WNDR3700V4:
    NETGEAR WNDR3700v4
    Packages: kmod-usb-core kmod-usb2 kmod-usb-ledtrig-usbport
```

## PACKAGES

检查默认的 Packages, 删除或添加软件源中的 Packages.

```shell
replace_ipks=(
    -dnsmasq
    dnsmasq-full
)
luci_ipks=(
    luci
    luci-i18n-base-zh-cn
    luci-i18n-firewall-zh-cn
)
zjuvpn_ipks=(
    kmod-l2tp
    kmod-pppol2tp
    ppp-mod-pppol2tp
    xl2tpd
)
other_ipks=(
    htop iftop ip shadow-su shadow-useradd ss
    luci-app-ddns luci-i18n-ddns-zh-cn
    luci-app-qos luci-i18n-qos-zh-cn
    luci-app-samba luci-i18n-samba-zh-cn
    luci-app-sqm
    luci-app-statistics luci-i18n-statistics-zh-cn
    luci-app-watchcat luci-i18n-watchcat-zh-cn
    luci-app-wol luci-i18n-wol-zh-cn
    #luci-app-privoxy luci-i18n-privoxy-zh-cn
    #luci-app-tinyproxy  luci-i18n-tinyproxy-zh-cn
    #luci-app-minidlna luci-i18n-minidlna-zh-cn
    #luci-app-upnp luci-i18n-upnp-zh-cn
    aria2 ariang
    #yaaw
    ca-certificates # for aria2 verify https
    transmission-daemon-mbedtls transmission-web
    luci-app-transmission luci-i18n-transmission-zh-cn
    autossh
    #sshfs
    #openssh-client # conflict: dropbear, /usr/bin/ssh -> /sbin/dropbear
    nfs-kernel-server-utils # cmd: nfsstat showmount
    shadowsocks-libev-ss-{server,redir,tunnel,rules,local} luci-app-shadowsocks-libev
    )
```

添加 USB 存储。

> 关于 [block-mount](https://openwrt.org/docs/techref/block_mount)

> `block-mount_2018-04-16-e2436836-1` `block info` 可以检测到的[文件系统](https://git.openwrt.org/?p=project/fstools.git;a=tree;f=libblkid-tiny;h=7d5e866db06868f42568fb0dbdc8431f2ca91976;hb=e24368361db166cf369a19cea773bd54f9d854b1)

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
    adbyby luci-app-adbyby-plus luci-i18n-adbyby-plus-zh-cn
    #frpc frps
    vlmcsd luci-app-vlmcsd
    nginx
    luci-app-aria2 luci-i18n-aria2-zh-cn
    luci-app-autossh luci-i18n-autossh-zh-cn
    luci-app-nfs luci-i18n-nfs-zh-cn
)
```


## 编译

```shell
$ cd /home/openwrt/imagebuilder/
$ make image \
  PROFILE=WNDR3700V4 \
  PACKAGES="$(echo\
    ${replace_ipks[@]}\
    ${luci_ipks[@]}\
    ${zjuvpn_ipks[@]}\
    ${other_ipks[@]}\
    ${usb_ipks[@]}\
    ${my_ipks[@]})" \
  FILES="/home/openwrt/myfiles_for_image"
```

生成的镜像位置 `/home/openwrt/imagebuilder/bin/targets/ar71xx/nand/`,
文件名 `openwrt-18.06.1-ar71xx-nand-wndr3700v4-ubi-factory.img`.
