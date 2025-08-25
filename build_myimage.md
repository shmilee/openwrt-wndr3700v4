# 编译 WNDR3700v4 固件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

## 准备 ImageBuilder

* 下载 [ImageBuilder](https://openwrt.proxy.ustclug.org/releases/24.10.2/targets/ath79/nand/openwrt-imagebuilder-24.10.2-ath79-nand.Linux-x86_64.tar.zst)
* 检查MD5, 解压 -> `work/imagebuilder-xx.xx.x-ath79-nand`

## 准备软件源

* 用 mirror-tools 下载官方缓慢的源到本地位置,
  如 `./mirror-tools/{openwrt-24.10.2,openwrt-packages-24.10}`.

* 依照 [build_mypackage](./build_mypackage.md) 编译软件包,
  生成的 ipk, `package_index` 放到 `./mypackages`

* 签名 `./mypackages/Packages`
  ```
  DISTRIB_RELEASE="24.10.2"
  USIGN=./work/imagebuilder-$DISTRIB_RELEASE-ath79-nand/staging_dir/host/bin/usign
  BUILD_KEY=./work/imagebuilder-$DISTRIB_RELEASE-ath79-nand/key-build
  "$USIGN" -S -m ./mypackages/Packages -s "$BUILD_KEY"
  ```

* 修改软件源 `work/imagebuilder-xx.xx.x-ath79-nand/repositories.conf`.  
  假设 `./mirror-tools` 对应 `/mnt`,  
  `./mypackages` 对应 `/home/openwrt/mypackages` :

```shell
src/gz openwrt_core file:///mnt/openwrt-24.10.2/targets/ath79/nand/packages
src/gz openwrt_base file:///mnt/openwrt-packages-24.10/mips_24kc/base
src/gz openwrt_kmods file:///mnt/openwrt-24.10.2/targets/ath79/nand/kmods/6.6.93-1-ba16238a7a163b7e7c5402245d60bef1
src/gz openwrt_luci file:///mnt/openwrt-packages-24.10/mips_24kc/luci
src/gz openwrt_packages file:///mnt/openwrt-packages-24.10/mips_24kc/packages
src/gz openwrt_routing file:///mnt/openwrt-packages-24.10/mips_24kc/routing
src/gz openwrt_telephony file:///mnt/openwrt-packages-24.10/mips_24kc/telephony
src/gz mypackages file:///home/openwrt/mypackages
src imagebuilder file:packages
```

## 准备自定义配置

所有修改过的配置, 标记替换敏感信息放入 `./custom-files-templates/` 作为模板.

**用 `myfiles-secret.py` 保存个人敏感信息**, 一个示例 `myfiles-secret-example.py`.

运行 `gen_myfiles.py`, 依照模板生成自定义配置 `myfiles_for_image/`.

```shell
cd ./custom-files-templates/
# gpg -e -r username -a myfiles-secret.py
gpg -d myfiles-secret.py.asc > myfiles-secret.py
./gen_myfiles.py myfiles-secret.py
cd ../
```

## 关于 128M flash layout

1. openwrt [flash layout 的介绍文档](https://openwrt.org/docs/techref/flash.layout)

2. 刷使用默认分区布局的固件，ssh 登录路由，查看固件信息。
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

root@OpenWrt:~# ls /dev/ubi*
/dev/ubi0         /dev/ubi0_0       /dev/ubi0_1       /dev/ubi_ctrl     /dev/ubiblock0_0

root@OpenWrt:~# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                13.8M     13.8M         0 100% /rom
tmpfs                    58.7M    864.0K     57.9M   1% /tmp
/dev/ubi0_1              87.6M     72.0K     83.0M   0% /overlay
overlayfs:/overlay       87.6M     72.0K     83.0M   0% /
tmpfs                   512.0K         0    512.0K   0% /dev
```

因此 24.10.x 已充分利用了 128M 的闪存。
仅当编译的固件体积过大时，才需要考虑修改 layout。
比如，固件中加入了go编译的较大软件包，才需重点检查 kernel+firmware 的体积。

3. 修改 layout 的相关文件。

* `target/linux/ath79/dts/ar9344_netgear_wndr.dtsi`

4. 修改 128M layout 的相关参考链接：
    - https://blog.csdn.net/u011570312/article/details/112269634
    - https://www.red-yellow.net/netgear-wndr3700-v4%E5%88%B7openwrt%E5%9B%BA%E4%BB%B6.html
    - dts [设备树介绍](https://cloud.tencent.com/developer/article/2008640)

5. Optional，对比旧版 [19.07.x 的分区布局](./backup_19.07.x_layout.md)。

## 进入 `Docker container`

```
docker run --rm -i -t -u openwrt \
    -w /home/openwrt/imagebuilder \
    -v $PWD/work/imagebuilder-24.10.2-ath79-nand:/home/openwrt/imagebuilder \
    -v $PWD/mirror-tools:/mnt \
    -v $PWD/mypackages:/home/openwrt/mypackages \
    -v $PWD/myfiles_for_image:/home/openwrt/myfiles_for_image \
    shmilee/openwrt-buildsystem:24.10.x /bin/bash
```

**以下命令默认在 `container` 中运行**。

## PROFILE

查看 Profile `NETGEAR WNDR3700v4`.

```shell
$ cd /home/openwrt/imagebuilder/
$ make info
Current Target: "ath79/nand"
Current Architecture: "mips"
Current Revision: "r28739-d9340319c6"
Default Packages: base-files ca-bundle dropbear fstools libc libgcc libustream-mbedtls logd mtd netifd uci uclient-fetch urandom-seed urngd kmod-gpio-button-hotplug swconfig kmod-ath9k uboot-envtools wpad-basic-mbedtls procd-ujail dnsmasq firewall4 nftables kmod-nft-offload odhcp6c odhcpd-ipv6only ppp ppp-mod-pppoe opkg

netgear_wndr3700-v4:
    NETGEAR WNDR3700 v4
    Packages: kmod-usb2 kmod-usb-ledtrig-usbport
    hasImageMetadata: 1
    SupportedDevices: netgear,wndr3700-v4
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
vpn_ipks=(
    kmod-l2tp
    kmod-pppol2tp
    ppp-mod-pppol2tp
    xl2tpd
)
other_ipks=(
    htop iftop ip kmod-sit shadow-su shadow-useradd ss
    luci-app-ddns luci-i18n-ddns-zh-cn
    luci-app-qos luci-i18n-qos-zh-cn
    #luci-app-samba4 luci-i18n-samba4-zh-cn
    luci-app-sqm
    luci-app-statistics luci-i18n-statistics-zh-cn
    luci-app-watchcat luci-i18n-watchcat-zh-cn
    luci-app-wol luci-i18n-wol-zh-cn
    #luci-app-privoxy luci-i18n-privoxy-zh-cn
    #luci-app-tinyproxy  luci-i18n-tinyproxy-zh-cn
    #luci-app-minidlna luci-i18n-minidlna-zh-cn
    #luci-app-upnp luci-i18n-upnp-zh-cn
    aria2 ariang
    luci-app-aria2 luci-i18n-aria2-zh-cn
    ca-certificates # for aria2 verify https
    transmission-daemon transmission-web
    luci-app-transmission luci-i18n-transmission-zh-cn
    autossh openssh-client sshfs
    nfs-kernel-server-utils # cmd: nfsstat showmount
    nginx-ssl
)
big_ipks=(
    #adguardhome adblock luci-app-adblock
    #frpc luci-app-frpc luci-i18n-frpc-zh-cn
    #frps luci-app-frps luci-i18n-frps-zh-cn
    tailscale
    #v2raya luci-app-v2raya luci-i18n-v2raya-zh-cn
)
```

添加 USB 存储。

> 关于 [block-mount](https://openwrt.org/docs/techref/block_mount)

> `block-mount_2024.07.14~408c2cc4-r1` `block info` 可以检测到的[文件系统](https://git.openwrt.org/?p=project/fstools.git;a=tree;f=libblkid-tiny;h=e904c5305eb1c4f46a0ef5600e8b9c74b976a2df;hb=408c2cc48e6694446c89da7f8121b399063e1067)

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
    vlmcsd luci-app-vlmcsd luci-i18n-vlmcsd-zh-cn
    luci-app-autossh luci-i18n-autossh-zh-cn
    luci-app-nfs luci-i18n-nfs-zh-cn
)
```


## 编译

```shell
$ cd /home/openwrt/imagebuilder/
$ make image \
  PROFILE=netgear_wndr3700-v4 \
  PACKAGES="$(echo\
    ${replace_ipks[@]}\
    ${luci_ipks[@]}\
    ${vpn_ipks[@]}\
    ${other_ipks[@]}\
    ${big_ipks[@]}\
    ${usb_ipks[@]}\
    ${my_ipks[@]})" \
  FILES="/home/openwrt/myfiles_for_image"
```

生成的镜像位置 `/home/openwrt/imagebuilder/bin/targets/ath79/nand/`,
文件名 `openwrt-xx.xx.x-ath79-nand-netgear_wndr3700-v4-squashfs-factory.img`.

