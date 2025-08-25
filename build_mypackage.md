# 编译 openwrt-shmilee-feeds 中的软件

## 准备 Docker image

* 依照 [OpenWrt-buildsystem](./openwrt-buildsystem/readme.md) 构建编译环境。

* 下载 [SDK](https://openwrt.proxy.ustclug.org/releases/24.10.2/targets/ath79/nand/openwrt-sdk-24.10.2-ath79-nand_gcc-13.3.0_musl.Linux-x86_64.tar.zst) -> 解压到 `work/sdk-xx.xx.x-ath79-nand`

* 编辑 `work/sdk-xx.xx.x-ath79-nand/feeds.conf.default`
  ```
  src-git base https://git.openwrt.org/openwrt/openwrt.git;openwrt-24.10
  src-git packages https://git.openwrt.org/feed/packages.git^c7d1a8c1ae976bd0ad94a351d82ee8fbf16a81f0
  src-git luci https://git.openwrt.org/project/luci.git^d6b13f648339273facc07b173546ace459c1cabe
  src-git shmilee https://github.com/shmilee/openwrt-shmilee-feeds.git
  ```

* 进入 `Docker container`
  ```
  docker run --rm -i -t --network=host -u openwrt \
    -v $PWD/work/sdk-24.10.2-ath79-nand:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:24.10.x /bin/bash
  ```

* 在 container 内更新 & 查看 `feeds`
  ```
  ./scripts/feeds update -a
  #./scripts/feeds update -i shmilee # update index after changes
  ./scripts/feeds list -r shmilee
  ```

## 在 container 内编译软件

1. `vlmcsd`

   ```shell
   ./scripts/feeds install -p shmilee vlmcsd
   make package/vlmcsd/compile V=sw
   ```

2. prepare `po2lmo`

   ```
   ./scripts/feeds install luci-base
   make package/luci-base/compile
   ```

    or

   ```
   cd ./feeds/luci/
   cat docs/i18n.md

   cd modules/luci-base/src/
   make po2lmo
   install -Dm755 po2lmo ~/sdk/staging_dir/hostpkg/bin/po2lmo
   make clean
   rm po2lmo po2lmo.o

   cd ~/sdk
   ```

3. `luci-*`

   ```shell
   ./scripts/feeds install -p shmilee \
       luci-app-autossh \
       luci-app-nfs \
       luci-app-vlmcsd
   ./scripts/feeds uninstall linux \
       dnsmasq gmp ipset iwinfo libjson-c libmnl libubox lua rpcd ubus uci \
       luci-lib-ip luci-lib-nixio \
       autossh nfs-kernel-server ustream-ssl uclient
   ./scripts/feeds uninstall libmd libnl-tiny \
       ucode lucihttp rpcd-mod-luci ucode-mod-html cgi-io csstidy \
       luasrcdiet luci-base luci-lib-base luci-lib-jsonc luci-lua-runtime lua ucode-mod-lua

   make package/luci-app-autossh/compile V=sw
   make package/luci-app-nfs/compile V=sw
   make package/luci-app-vlmcsd/compile V=sw
   ```

# container generating package index

1. 生成的软件包所在目录 `work/sdk-xx.xx.x-ath79-nand/bin/packages/mips_24kc/shmilee/`

```
luci-app-autossh_1.0.0-r1_all.ipk
luci-app-nfs_1.0.0-r2_all.ipk
luci-app-vlmcsd_1.0.1-r1_all.ipk
luci-i18n-autossh-zh-cn_25.237.15863~a0ddb80_all.ipk
luci-i18n-nfs-zh-cn_25.237.15863~a0ddb80_all.ipk
luci-i18n-vlmcsd-zh-cn_25.237.15863~a0ddb80_all.ipk
vlmcsd_2020.09.16~ae16d038-r2_mips_24kc.ipk
```

2. make index

```
make package/index V=sc
```

or

```
export MKHASH=/home/openwrt/sdk/staging_dir/host/bin/mkhash
Scripts=/home/openwrt/sdk/scripts

cd /home/openwrt/sdk/bin/packages/mips_24kc/shmilee
$Scripts/ipkg-make-index.sh . > Packages.manifest

grep -vE '^(Maintainer|LicenseFiles|Source|SourceName|Require|SourceDateEpoch)' Packages.manifest > Packages
case "$$(((64 + $$(stat -L -c%s Packages)) % 128))" in 110|111)
    echo "ERROR_MESSAGE,WARNING: Applying padding in $subdir/Packages to workaround usign SHA-512 bug!"
    { echo ""; echo ""; } >> Packages
esac

gzip -9nc Packages > Packages.gz

ARCH_PACKAGES="mips_24kc"
$Scripts/make-index-json.py -f opkg -a "${ARCH_PACKAGES}" Packages > index.json
```
