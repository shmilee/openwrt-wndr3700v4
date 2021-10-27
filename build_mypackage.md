# 编译 openwrt-shmilee-feeds 中的软件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

* 下载 [SDK](https://openwrt.proxy.ustclug.org/releases/21.02.0/targets/ath79/nand/openwrt-sdk-21.02.0-ath79-nand_gcc-8.4.0_musl.Linux-x86_64.tar.xz) -> 解压到 `work/sdk-xx.xx.x-ath79-nand`

* 编辑 `work/sdk-xx.xx.x-ath79-nand/feeds.conf.default`
  ```
  src-git base https://git.openwrt.org/openwrt/openwrt.git;v21.02.0
  src-git packages https://git.openwrt.org/feed/packages.git^65057dcbb5de371503c9159de3d45824bec482e0
  src-git luci https://git.openwrt.org/project/luci.git^3b3c2e5f9f82372df8ff01ac65668be47690dcd5
  src-git shmilee https://github.com/shmilee/openwrt-shmilee-feeds.git
  ```

* 进入 `Docker container`
  ```
  docker run --rm -i -t --network=host -u openwrt \
    -v $PWD/work/sdk-21.02.0-ath79-nand:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:21.02.x /bin/bash
  ```

* 在 container 内更新 `feeds`
  ```
  ./scripts/feeds update -a
  ```

## 在 container 内编译软件

生成的软件包所在目录 `work/sdk-xx.xx.x-ath79-nand/bin/packages/mips_24kc/shmilee/`

1. `adbyby`, `adbyby_2.7-20200315_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee adbyby
   make package/adbyby/compile V=sw
   ```

2. `radvd`, `radvd_2.17-1_mips_24kc.ipk`, `radvdump_2.17-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee radvd
   make package/radvd/compile V=sw
   ```

3. `frp`, `frpc_0.37.1-1_mips_24kc.ipk`, `frps_0.37.1-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -f -p shmilee frpc frps
   make package/frp/compile V=sw
   ```

4. `vlmcsd`, `vlmcsd_svn1112-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee vlmcsd
   make package/vlmcsd/compile V=sw
   ```

5. `nginx`, `nginx-all-module_1.19.6-1_mips_24kc.ipk`,
   `nginx-mod-luci-ssl_1.19.6-1_all.ipk`, `nginx-mod-luci_1.19.6-1_mips_24kc.ipk`,
   `nginx-ssl_1.19.6-1_mips_24kc.ipk`, `nginx_1.19.6-1_all.ipk`

   ```shell
   ./scripts/feeds install -p shmilee nginx
   make package/nginx/compile V=sw
   ```

6. `luci-*`

   ```
   luci-app-adbyby-plus_2.0_all.ipk
   luci-app-autossh_1.0.0_all.ipk
   luci-app-nfs_1.0.0_all.ipk
   luci-app-vlmcsd_1.0.1-1_all.ipk
   luci-i18n-adbyby-plus-zh-cn_git-21.299.59620-0a11db1_all.ipk
   luci-i18n-autossh-zh-cn_git-21.299.59620-0a11db1_all.ipk
   luci-i18n-nfs-zh-cn_git-21.299.59620-0a11db1_all.ipk
   ```

   ```shell
   ./scripts/feeds install -p shmilee \
       luci-app-adbyby-plus \
       luci-app-autossh \
       luci-app-nfs \
       luci-app-vlmcsd
   ./scripts/feeds uninstall linux \
       dnsmasq gmp ipset iwinfo libjson-c libmnl libubox lua rpcd ubus uci \
       luci-lib-ip luci-lib-nixio \
       autossh nfs-kernel-server ustream-ssl uclient
   make package/luci-app-adbyby-plus/compile V=sw
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
