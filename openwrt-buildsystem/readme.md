Build Docker image
==================

```
docker build --force-rm --no-cache --rm -t shmilee/openwrt-buildsystem:21.02.x .
```

Use Docker image
================

* https://openwrt.org/docs/guide-developer/start
* https://openwrt.org/docs/guide-developer/build-system/use-buildsystem

__User=openwrt, UID=1000, Group=users, GID=100__

* Download SDK, for [example](https://openwrt.proxy.ustclug.org/releases/21.02.0/targets/ath79/nand/openwrt-sdk-21.02.0-ath79-nand_gcc-8.4.0_musl.Linux-x86_64.tar.xz)
* decompress -> `openwrt-sdk`

```
chown -R 1000:100 openwrt-sdk/

docker run --rm -i -t -u openwrt \
    -v $PWD/openwrt-sdk:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:21.02.x /bin/bash

# maybe needed, add PATH in container
#export PATH=/home/openwrt/sdk/staging_dir/toolchain-<platform>-<gcc_ver>-<libc_ver>/bin:$PATH
```
