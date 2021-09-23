Build Docker image
==================

```
docker build --force-rm --no-cache --rm -t shmilee/openwrt-buildsystem:19.07.8 .
```

Use Docker image
================

* https://openwrt.org/docs/guide-developer/start
* https://openwrt.org/docs/guide-developer/build-system/use-buildsystem

__User=openwrt, UID=1000, Group=users, GID=100__

* Download SDK, for [example](https://mirrors.ustc.edu.cn/openwrt/releases/19.07.8/targets/ar71xx/nand/openwrt-sdk-19.07.8-ar71xx-nand_gcc-7.5.0_musl.Linux-x86_64.tar.xz)
* decompress -> `openwrt-sdk`

```
chown -R 1000:100 openwrt-sdk/

docker run --rm -i -t -u openwrt \
    -v $PWD/openwrt-sdk:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:19.07.8 /bin/bash

# maybe needed, add PATH in container
#export PATH=/home/openwrt/sdk/staging_dir/toolchain-<platform>-<gcc_ver>-<libc_ver>/bin:$PATH
```
