# 编译 openwrt-shmilee-feeds 中的软件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

* 下载 [SDK](https://mirrors.ustc.edu.cn/openwrt/releases/19.07.8/targets/ar71xx/nand/openwrt-sdk-19.07.8-ar71xx-nand_gcc-7.5.0_musl.Linux-x86_64.tar.xz) -> 解压到 `work/sdk-xx.xx.x-ar71xx-nand`

* 编辑 `work/sdk-xx.xx.x-ar71xx-nand/feeds.conf.default`
  ```
  src-git base https://git.openwrt.org/openwrt/openwrt.git;v19.07.8
  src-git packages https://git.openwrt.org/feed/packages.git^c6ae1c6a0fced32c171e228e3425a9b655585011
  src-git luci https://git.openwrt.org/project/luci.git^7b931da4779c68f5aef5908286c2ae5283d2dece
  src-git shmilee https://github.com/shmilee/openwrt-shmilee-feeds.git
  ```

* 进入 `Docker container`
  ```
  docker run --rm -i -t -u openwrt \
    -v $PWD/work/sdk-19.07.8-ar71xx-nand:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:19.07.8 /bin/bash
  ```

* 在 container 内更新 `feeds`
  ```
  ./scripts/feeds update -a
  ```

## 在 container 内编译软件

生成的软件包所在目录 `work/sdk-xx.xx.x-ar71xx-nand/bin/packages/mips_24kc/shmilee/`

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

5. `nginx`, `nginx_1.12.2-1_mips_24kc.ipk`

   ```shell
   ./scripts/feeds install -p shmilee nginx
   make package/nginx/compile V=sw
   ```

6. `luci-*`

   ```
   luci-app-adbyby-plus_2.0-75_all.ipk
   luci-app-autossh_1.0.0-1_all.ipk
   luci-app-nfs_1.0.0-2_all.ipk
   luci-app-vlmcsd_1.0.1-1_all.ipk
   luci-i18n-adbyby-plus-zh-cn_2.0-75_all.ipk
   luci-i18n-autossh-zh-cn_1.0.0-1_all.ipk
   luci-i18n-nfs-zh-cn_1.0.0-2_all.ipk
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
