Build Docker image
==================

```
docker build --force-rm --no-cache --rm -t shmilee/openwrt-buildsystem:18.06.1 .
```

Use Docker image
================

* https://openwrt.org/docs/guide-developer/start
* https://openwrt.org/docs/guide-developer/build-system/use-buildsystem

__User=openwrt, UID=1000, Group=users, GID=100__

* Download SDK, for [example](http://openwrt.proxy.ustclug.org/releases/18.06.1/targets/ar71xx/nand/openwrt-sdk-18.06.1-ar71xx-nand_gcc-7.3.0_musl.Linux-x86_64.tar.xz)
* decompress -> `openwrt-sdk`

```
chown -R 1000:100 openwrt-sdk/

docker run --rm -i -t -u openwrt \
    -v $PWD/openwrt-sdk:/home/openwrt/sdk \
    shmilee/openwrt-buildsystem:18.06.1 /bin/bash

# maybe needed, add PATH in container
#export PATH=/home/openwrt/sdk/staging_dir/toolchain-<platform>-<gcc_ver>-<libc_ver>/bin:$PATH
```
