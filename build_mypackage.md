# 编译 openwrt-shmilee-feeds 中的软件

## 准备 Docker image

* 依照 [OpenWrt-build-system-host](./OpenWrt-build-system-host/readme.md) 构建编译环境。

* 下载 [SDK](http://openwrt.proxy.ustclug.org/chaos_calmer/15.05.1/ar71xx/nand/OpenWrt-SDK-15.05.1-ar71xx-nand_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64.tar.bz2) -> 解压到 `work/SDK-15.05.1-ar71xx-nand`

* 编辑 `work/SDK-15.05.1-ar71xx-nand/feeds.conf.default`
  ```
  src-git base https://git.openwrt.org/15.05/openwrt.git
  src-git packages https://github.com/openwrt/packages.git;for-15.05
  src-git luci https://github.com/openwrt/luci.git;for-15.05
  src-git shmilee https://github.com/shmilee/openwrt-shmilee-feeds.git  
  ```

* 进入 `Docker container`
  ```
  docker run --rm -i -t -u openwrt \
    -v $PWD/work/SDK-15.05.1-ar71xx-nand:/home/openwrt/sdk \
    shmilee/openwrt-sdk-host:15.05.1 /bin/bash
  ```

* 在 container 内更新 `feeds`
  ```
  ./scripts/feeds update -a
  ```

## 在 container 内编译软件

生成的软件包所在目录 `work/SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/shmilee/`

1. `auotssh`, `autossh_1.4e-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee autossh
   # 编译
   # make package/autossh/prepare
   make package/autossh/compile V=sw
   # make package/autossh/install
   ```

2. `nginx`, `nginx_1.12.2-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee nginx
   make package/nginx/compile V=sw
   ```

3. `aria2`, `aria2_1.33.0-1_ar71xx.ipk`

   `yaaw`, `yaaw_2017-04-11-1_all.ipk`

   `ariang`, `ariang_0.3.0-1_all.ipk`

   ```shell
   ./scripts/feeds install -p shmilee aria2 yaaw ariang
   make package/aria2/compile V=sw
   make package/yaaw/compile V=sw
   make package/ariang/compile V=sw
   ```

4. `vlmcsd`, `vlmcsd_svn1111-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee vlmcsd
   make package/vlmcsd/compile V=sw
   ```

5. `miredo`, `miredo-common_1.2.6-1_ar71xx.ipk`,
   `miredo-client_1.2.6-1_ar71xx.ipk`, `miredo-server_1.2.6-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee miredo-client miredo-server
   rm -v package/feeds/base/linux{,-firmware}
   make package/miredo/compile V=sw
   ```

6. `shadowsocks-libev`,
   `shadowsocks-libev-server_3.1.1-1_ar71xx.ipk`, `shadowsocks-libev_3.1.1-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee shadowsocks-libev
   make package/shadowsocks-libev/compile V=sw
   ```

7. `adbyby`, `adbyby_2.7-20170823_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee adbyby
   make package/adbyby/compile V=sw
   ```

8. `goagent-client`, `goagent-client_3.2.3.20150617-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -p shmilee goagent-client
   make package/goagent-client/compile V=sw
   ```

9. `frp`, `frpc_0.14.1-1_ar71xx.ipk`, `frps_0.14.1-1_ar71xx.ipk`

   ```shell
   ./scripts/feeds install -f -p shmilee frpc frps
   make package/frp/compile V=sw
   ```

10. `luci-app-*`

   ```
   luci-app-adbyby-plus_2.0-25_all.ipk
   luci-app-aria2_1.0.1-2_all.ipk
   luci-app-autossh_1.0.0-1_all.ipk
   luci-app-nfs_1.0.0-1_all.ipk
   luci-app-shadowsocks-without-ipset_1.8.2-1_all.ipk
   luci-app-shadowsocks_1.8.2-1_all.ipk
   luci-app-vlmcsd_1.0.1-1_all.ipk
   luci-i18n-adbyby-plus-zh-cn_2.0-25_all.ipk
   luci-i18n-aria2-pt-br_1.0.1-2_all.ipk
   luci-i18n-aria2-sv_1.0.1-2_all.ipk
   luci-i18n-aria2-zh-cn_1.0.1-2_all.ipk
   luci-i18n-aria2-zh-tw_1.0.1-2_all.ipk
   luci-i18n-autossh-zh-cn_1.0.0-1_all.ipk   
   luci-i18n-nfs-zh-cn_1.0.0-1_all.ipk
   ```

   ```shell
   ./scripts/feeds install -p shmilee \
       luci-app-autossh \
       luci-app-aria2 \
       luci-app-vlmcsd \
       luci-app-shadowsocks \
       luci-app-adbyby-plus \
       luci-app-nfs
   rm -v package/feeds/base/{gmp,linux{,-firmware},cyassl}
   ./scripts/feeds uninstall dnsmasq ipset iptables wget \
       lua luci-base uci luci-lib-nixio luci-lib-ip \
       libubox libjson-c rpcd ubus iwinfo libmnl nfs-kernel-server
   make package/luci-app-autossh/compile V=sw
   make package/luci-app-aria2/compile V=sw
   make package/luci-app-vlmcsd/compile V=sw
   make package/luci-app-shadowsocks/compile V=sw
   make package/luci-app-adbyby-plus/compile V=sw
   make package/luci-app-nfs/compile V=sw
   ```


