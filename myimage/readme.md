# 准备 ImageBuilder

* [下载](http://openwrt.proxy.ustclug.org/chaos_calmer/15.05.1/ar71xx/nand/OpenWrt-ImageBuilder-15.05.1-ar71xx-nand.Linux-x86_64.tar.bz2)
* 检查MD5: 74af3f78e2d7d4fdc7d65c1ed21a6c78
* 解压 -> `ImageBuilder-15.05.1-ar71xx-nand`
* 修改软件源 `ImageBuilder-15.05.1-ar71xx-nand/repositories.conf`  
  用 mirror url, 或 mirror-tools 下载到本地的位置 替换官方缓慢的源。  
  一个例子：

```shell
src/gz chaos_calmer_base file:../../mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand/packages/base
src/gz chaos_calmer_luci file:../../mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand/packages/luci
src/gz chaos_calmer_packages file:../../mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand/packages/packages
src/gz chaos_calmer_routing file:../../mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand/packages/routing
src/gz chaos_calmer_management file:../../mirror-tools/openwrt-ipks-15.05.1/ar71xx/nand/packages/management
src imagebuilder file:packages
```

# 编译固件

## 128M flash

修改 `ImageBuilder-15.05.1-ar71xx-nand/target/linux/ar71xx/image/Makefile`
中以 `wndr4300_mtdlayout` 开头的行, 尽量多的使用 128M nand flash.
[1](https://wiki.openwrt.org/doc/techref/flash.layout)

```shell
## firmware = kernel + ubi, kernel is 2048k
$ cat /proc/cmdline 
 board=WNDR3700_V4 console=ttyS0,115200 mtdparts=ar934x-nfc:256k(u-boot)ro,
256k(u-boot-env)ro,256k(caldata),512k(pot),2048k(language),512k(config),
3072k(traffic_meter),2048k(kernel),23552k(ubi),25600k@0x6c0000(firmware),
256k(caldata_backup),-(reserved) rootfstype=squashfs noinitrd

以下是官方固件的信息:

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
```

最大利用: name9 + name 11 = 123904(121M) -> firmware, 123904 - name7 = 121856 -> ubi

保守点:

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

cd ImageBuilder-15.05.1-ar71xx-nand/target/linux/ar71xx/image/
cp Makefile Makefile.bk
sed -i "s/\(^wndr4300_mtdlayout.*\)23552k\(.ubi..\)25600k\(.*$\)/\1${ubi}k\2${firmware}k\3/" Makefile
```

## Profiles

查看支持的 Profiles. NETGEAR WNDR3700v4/WNDR430 共用一个 Profile.

```shell
$ cd ImageBuilder-15.05.1-ar71xx-nand/
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

自己编译的的 Package 放到目录 `ImageBuilder-15.05.1-ar71xx-nand/packages`.

```shell
find ../mypackages -name '*.ipk' -exec \
    cp -v {} packages/ \;
my_ipks=(
    adbyby luci-app-adbyby
    aria2 luci-app-aria2 luci-i18n-aria2-zh-cn
    ariang
    autossh
    nginx
    shadowsocks-libev luci-app-shadowsocks
    vlmcsd luci-app-vlmcsd
    #yaaw
)
```

## 添加自定义配置

所有修改过的配置, 按相应路径放入 `myfiles_templates/`, 这里相当于 `root /`.

~~从 static-routes 选取一份静态路由,~~
~~编辑 gateway 后添加到 `3700v4_files/etc/config/network`.~~

**用 `myfiles_secret.py` 保存个人相关信息**, 一个示例 `myfiles_secret-example.py`.

运行 `gen_myfiles.py`, 自动修改 `myfiles_templates/` 生成 自定义配置 `myfiles_for_image/`

```shell
cd myfiles_templates/
gpg -d myfiles_secret.py.asc > myfiles_secret.py
./gen_myfiles.py
cd ../
```

## 编译

```shell
cd ImageBuilder-15.05.1-ar71xx-nand/
make image \
  PROFILE=WNDR4300 \
  PACKAGES="$(echo\
    ${replace_ipks[@]}\
    ${luci_ipks[@]}\
    ${zjuvpn_ipks[@]}\
    ${usb_ipks[@]}\
    ${other_ipks[@]}\
    ${my_ipks[@]})" \
  FILES="../myfiles_for_image"
```

生成的镜像位置 `ImageBuilder-15.05.1-ar71xx-nand/bin/ar71xx/`,
文件名 `openwrt-15.05.1-ar71xx-nand-wndr3700v4-ubi-factory.img`.
