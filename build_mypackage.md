# 编译 openwrt-shmilee-feeds 中的软件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

* 下载 [SDK](http://openwrt.proxy.ustclug.org/releases/18.06.1/targets/ar71xx/nand/openwrt-sdk-18.06.1-ar71xx-nand_gcc-7.3.0_musl.Linux-x86_64.tar.xz) -> 解压到 `work/sdk-18.06.1-ar71xx-nand`

* 编辑 `work/sdk-18.06.1-ar71xx-nand/feeds.conf.default`
  ```
  src-git base https://git.openwrt.org/openwrt/openwrt.git;v18.06.1
  src-git packages https://git.openwrt.org/feed/packages.git^35e0b737ab496f5b51e80079b0d8c9b442e223f5
  src-git luci https://git.openwrt.org/project/luci.git^f64b1523447547032d5280fb0bcdde570f2ca913
  src-git shmilee https://github.com/shmilee/openwrt-shmilee-feeds.git
  ```

* 进入 `Docker container`
  ```
  docker run --rm -i -t -u openwrt \
    -v $PWD/work/sdk-18.06.1-ar71xx-nand:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:18.06.1 /bin/bash
  ```

* 在 container 内更新 `feeds`
  ```
  ./scripts/feeds update -a
  ```

## 在 container 内编译软件

生成的软件包所在目录 `work/sdk-18.06.1-ar71xx-nand/bin/packages/mips_24kc/shmilee/`

1. `adbyby`, `adbyby_2.7-20180616_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee adbyby
   make package/adbyby/compile V=sw
   ```

2. `frp`, `frpc_0.21.0-1_mips_24kc.ipk`, `frps_0.21.0-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -f -p shmilee frpc frps
   make package/frp/compile V=sw
   ```

3. `vlmcsd`, `vlmcsd_svn1111-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee vlmcsd
   make package/vlmcsd/compile V=sw
   ```

4. `nginx`, `nginx_1.12.2-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee nginx
   make package/nginx/compile V=sw
   ```

5. `luci-app-*`

   ```
   luci-app-adbyby-plus_2.0-29_all.ipk
   luci-app-aria2_1.0.1-2_all.ipk
   luci-app-autossh_1.0.0-1_all.ipk
   luci-app-nfs_1.0.0-2_all.ipk
   luci-app-vlmcsd_1.0.1-1_all.ipk
   luci-i18n-adbyby-plus-zh-cn_2.0-29_all.ipk
   luci-i18n-aria2-pt-br_1.0.1-2_all.ipk
   luci-i18n-aria2-ru_1.0.1-2_all.ipk
   luci-i18n-aria2-sv_1.0.1-2_all.ipk
   luci-i18n-aria2-zh-cn_1.0.1-2_all.ipk
   luci-i18n-aria2-zh-tw_1.0.1-2_all.ipk
   luci-i18n-autossh-zh-cn_1.0.0-1_all.ipk
   luci-i18n-nfs-zh-cn_1.0.0-2_all.ipk
   ```

   ```shell
   ./scripts/feeds install -p shmilee \
       luci-app-adbyby-plus \
       luci-app-aria2 \
       luci-app-autossh \
       luci-app-nfs \
       luci-app-vlmcsd
   ./scripts/feeds uninstall linux \
       dnsmasq gmp ipset iwinfo libjson-c libmnl libubox lua rpcd ubus uci \
       luci-lib-ip luci-lib-nixio \
       aria2 autossh coreutils nfs-kernel-server wget
   make package/luci-app-adbyby-plus/compile V=sw
   make package/luci-app-aria2/compile V=sw
   make package/luci-app-autossh/compile V=sw
   make package/luci-app-nfs/compile V=sw
   make package/luci-app-vlmcsd/compile V=sw
   ```

# container generating package index

  ```
  (cd /home/openwrt/sdk/bin/packages/mips_24kc/shmilee/ && \
    /home/openwrt/sdk/scripts/ipkg-make-index.sh . > Packages && \
    gzip -9c Packages > Packages.gz \
  )
  ```
