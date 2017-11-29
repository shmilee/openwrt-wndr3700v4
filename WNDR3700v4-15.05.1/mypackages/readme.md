# 准备 SDK

* [下载](http://openwrt.proxy.ustclug.org/chaos_calmer/15.05.1/ar71xx/nand/OpenWrt-SDK-15.05.1-ar71xx-nand_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64.tar.bz2)
* MD5: e1f64ce8f5612bb517762fde1eb0f507
* 解压 -> `SDK-15.05.1-ar71xx-nand`
* host os 安装需要的软件包. Archlinux(base-devel, ccache)

* https://wiki.openwrt.org/doc/howto/build
* https://wiki.openwrt.org/doc/techref/buildroot

# 编译 auotssh

下载并打补丁。打补丁主要是为了更灵活的使用 ssh 的端口转发(-L, -R, -D)。

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 获取 Makefile
git clone https://github.com/aa65535/openwrt-autossh.git package/autossh
# 打补丁
cd package/autossh
git checkout 34e7554
patch -p1 < ../../../mypackages/autossh/autossh-1.4e-34e7554.patch
cd ../../
```

如有下载的 autossh 源码包 `autossh-1.4e.tgz`,
可放置到 `SDK-15.05.1-ar71xx-nand/dl`.

```shell
# 选择要编译的包 Network -> SSH -> autossh
make menuconfig
# 编译
# make package/autossh/prepare
make package/autossh/compile V=sw
# make package/autossh/install
```
生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/autossh_1.4e-1_ar71xx.ipk`

# 编译 nginx

15.05.1 源里的 nginx 版本是 `1.4.7-2`, 未开启 `TLS SNI`.

这里编译 openwrt/packages master 分支最新的 [nginx](https://github.com/openwrt/packages/blob/master/net/nginx), 当前版本为 `1.10.1-2`.

开启 `TLS SNI`, 保留 `proxy module` 的同时, 尽量去除其他的 module,
如 autoindex, fastcgi, uwsgi, scgi, memcached, upstream hash, NAXSI 等.

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 安装 feeds
# backup: src-git masterpackages https://github.com/openwrt/packages.git^9b3666b
echo "src-git masterpackages https://github.com/openwrt/packages.git;master" \
    >> feeds.conf.default
./scripts/feeds update masterpackages
./scripts/feeds install -p masterpackages nginx
# patch
cp ../mypackages/nginx/1.10.1-2_Config.in \
    ./package/feeds/masterpackages/nginx/Config.in
cp ../mypackages/nginx/1.10.1-2_Makefile \
    ./package/feeds/masterpackages/nginx/Makefile
# 选择要编译的包 Network -> Web Servers/Proxies -> nginx
make menuconfig
# 编译
make package/nginx/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/masterpackages/nginx_1.10.1-2_ar71xx.ipk`

# 编译 shadowsocks-libev

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 安装 feeds
./scripts/feeds update packages
./scripts/feeds install libpcre
# 获取 Makefile
git clone https://github.com/shadowsocks/openwrt-shadowsocks.git package/shadowsocks-libev
# 选择要编译的包 Network -> shadowsocks-libev, shadowsocks-libev-server
# mbedTLS, PolarSSL 都不选
make menuconfig
# 编译
make package/shadowsocks-libev/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/shadowsocks-libev_2.5.6-1_ar71xx.ipk`
, `shadowsocks-libev-server_2.5.6-1_ar71xx.ipk`

# 编译 luci-app-shadowsocks

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# Clone 项目
git clone https://github.com/shadowsocks/luci-app-shadowsocks.git package/luci-app-shadowsocks
# 编译 po2lmo (如果有po2lmo可跳过, staging_dir/host/bin/po2lmo)
#pushd package/luci-app-shadowsocks/tools/po2lmo
#make && sudo make install
#popd
# 选择要编译的包 LuCI -> 3. Applications
make menuconfig
# 编译
make package/luci-app-shadowsocks/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/luci-app-shadowsocks_1.3.7-1_all.ipk`

# 编译 vlmcsd

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 获取 Makefile
git clone https://github.com/mchome/openwrt-vlmcsd.git package/vlmcsd
# 选择包 Network -> vlmcsd
make menuconfig
# 编译
make package/vlmcsd/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/vlmcsd_svn1016-1_ar71xx.ipk`

# 编译 luci-app-vlmcsd

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# Clone 项目
git clone https://github.com/mchome/luci-app-vlmcsd.git package/luci-app-vlmcsd
# 去掉依赖 dnsmasq, 防止与 dnsmasq-ful 冲突
sed -i 's/ +dnsmasq//' package/luci-app-vlmcsd/Makefile
# 分组 network -> services
sed -i 's/"network"/"services"/g' \
    package/luci-app-vlmcsd/files/luci/controller/vlmcsd.lua
# 选择包 LuCI -> 3. Applications -> luci-app-vlmcsd
make menuconfig
# 编译
make package/luci-app-vlmcsd/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/luci-app-vlmcsd_1.0.1-1_all.ipk`

# 编译 adbyby luci-app-adbyby

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 安装 feeds
./scripts/feeds update luci
# Clone 项目
git clone https://github.com/kuoruan/luci-app-adbyby.git dl-adbyby
mv dl-adbyby/adbyby package/
mv dl-adbyby/luci-app-adbyby feeds/luci/applications/
./scripts/feeds update luci
./scripts/feeds install luci-app-adbyby
./scripts/feeds uninstall luci-base wget
# 选择包 LuCI -> 3. Applications -> luci-app-adbyby
#        Network -> adbyby
make menuconfig
# 编译
make package/adbyby/compile V=sw
make package/luci-app-adbyby/compile V=sw
```
生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/base/adbyby_2.7-20160110_ar71xx.ipk`,
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/luci/luci-app-adbyby_git-16.313.39362-9047456-1_all.ipk`

# 编译 adblock luci-app-adblock

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 安装 feeds
./scripts/feeds update luci
./scripts/feeds install adblock luci-app-adblock
./scripts/feeds uninstall luci-base
# 选择包
make menuconfig
# 编译
make package/adblock/compile V=sw
make package/luci-app-adblock/compile V=sw
```

生成的软件包在
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/luci/luci-app-adblock_git-16.313.39362-9047456-1_all.ipk`,
`SDK-15.05.1-ar71xx-nand/bin/ar71xx/packages/packages/adblock_1.5.4-1_all.ipk`

# 编译 aria2 luci-app-aria2 yaaw AriaNg

* webui-aria2 体积太大

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# 安装 feeds
echo "src-git masterpackages https://github.com/openwrt/packages.git;master" \
    >> feeds.conf.default
# backup: src-git masterluci https://github.com/openwrt/luci.git^185e4c1 
echo "src-git masterluci https://github.com/openwrt/luci.git;master" \
    >> feeds.conf.default
./scripts/feeds update masterpackages
./scripts/feeds update masterluci
./scripts/feeds install -p masterpackages aria2 yaaw
./scripts/feeds install -p masterluci luci-app-aria2
./scripts/feeds uninstall luci-base
# 添加 AriaNg 到 luci-app-aria2
cd package/feeds/masterluci/luci-app-aria2
patch -p1 < ../../../../../mypackages/aria2/luci-app-aria2-185e4c1.patch
cd ../../../../
# 获取 AriaNg
install -Dm644 ../mypackages/aria2/ariang/Makefile package/feeds/masterpackages/ariang/Makefile
# 选择包
# Network > File Transfer > Aria2 configuration Enable bittorrent suppor
make menuconfig
# 编译
make package/aria2/compile V=sw
make package/yaaw/compile V=sw
make package/luci-app-aria2/compile V=sw
make package/ariang/compile V=sw
```

# 20171129, make ERROR because new perl

https://github.com/openwrt/packages/issues/4657

```
Unescaped left brace in regex is illegal here in regex; marked by <-- HERE in m/\${ <-- HERE ([^ \t=:+{}]+)}/ at /path/to/openwrt-backup/WNDR3700v4-15.05.1/SDK-15.05.1-ar71xx-nand/staging_dir/host/bin/automake-1.15 line 3938.
```

```
cd SDK-15.05.1-ar71xx-nand/
sed -i '/substitute_ac_subst_variables_worker/ s/\${/\$[{]/' staging_dir/host/bin/automake-1.15
```

Archlinux 不适合做 HOST OS, 暂时转 docker image, yhnw/openwrt-sdk:15.05.1-ar71xx 。

# 等待编译 miredo

```shell
# 进入 SDK
cd SDK-15.05.1-ar71xx-nand/
# Clone 项目
git clone openwrt-miredo.git  package/miredo
# 编译
make package/miredo/compile V=sw
```
生成的软件包在

