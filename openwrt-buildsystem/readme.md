Build Docker image
==================

```
docker build --force-rm --no-cache --rm -t shmilee/openwrt-buildsystem:24.10.x .
```

Use Docker image
================

* https://openwrt.org/docs/guide-developer/start
* https://openwrt.org/docs/guide-developer/build-system/use-buildsystem

__User=openwrt, UID=1000, Group=users, GID=100__

* Download SDK, for example [24.10.2](https://openwrt.proxy.ustclug.org/releases/24.10.2/targets/ath79/nand/openwrt-sdk-24.10.2-ath79-nand_gcc-13.3.0_musl.Linux-x86_64.tar.zst)
* decompress -> `openwrt-sdk`

```
chown -R 1000:100 openwrt-sdk/

docker run --rm -i -t -u openwrt \
    -v $PWD/openwrt-sdk:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:24.10.x /bin/bash

# maybe needed, add PATH in container
#PATH=/home/openwrt/sdk/staging_dir/host/bin:$PATH
#PATH=/home/openwrt/sdk/staging_dir/toolchain-<platform>-<gcc_ver>-<libc_ver>/bin:$PATH
#export PATH
```
