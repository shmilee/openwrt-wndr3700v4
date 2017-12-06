Build Docker image
==================

```
docker build --force-rm --no-cache --rm -t shmilee/openwrt-sdk-host:15.05.1 .
```

Use Docker image
================

* https://wiki.openwrt.org/doc/howto/build
* https://wiki.openwrt.org/doc/techref/buildroot

__User=openwrt, UID=1000, Group=users, GID=100__

An example:

* Download [SDK](http://openwrt.proxy.ustclug.org/chaos_calmer/15.05.1/ar71xx/nand/OpenWrt-SDK-15.05.1-ar71xx-nand_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64.tar.bz2), MD5: e1f64ce8f5612bb517762fde1eb0f507
* decompress -> `SDK-15.05.1-ar71xx-nand`

```
chown -R 1000:100 SDK-15.05.1-ar71xx-nand/

docker run --rm -i -t -u openwrt \
    -v $PWD/SDK-15.05.1-ar71xx-nand:/home/openwrt/sdk \
    shmilee/openwrt-sdk-host:15.05.1 /bin/bash

# maybe needed, add PATH in container
#export PATH=/home/openwrt/sdk/staging_dir/toolchain-<platform>-<gcc_ver>-<libc_ver>/bin:$PATH
```
