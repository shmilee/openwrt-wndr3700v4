# debian:stretch-20180716
# https://openwrt.org/docs/guide-developer/build-system/install-buildsystem

FROM debian:stretch

LABEL maintainer="shmilee.zju@gmail.com" \
      sdk.version="18.06.1" \
      description="Debian 9 with OpenWRT build system prerequisites"

ENV TIMEZONE=Asia/Shanghai \
    DEBIAN_CODENAME=stretch \
    DEBIAN_MIRROR=http://mirrors.163.com/debian \
    DEBIAN_SECURITY_MIRROR=http://mirrors.163.com/debian-security \
    PATH=/home/openwrt/sdk/staging_dir/host/bin:$PATH

COPY dpkg.cfg.excludes /etc/dpkg/dpkg.cfg.d/01_excludes

RUN echo "$TIMEZONE" > /etc/timezone \
 && echo "deb $DEBIAN_MIRROR $DEBIAN_CODENAME main" > /etc/apt/sources.list \
 && echo "deb $DEBIAN_MIRROR $DEBIAN_CODENAME-updates main" >> /etc/apt/sources.list \
 && echo "deb $DEBIAN_SECURITY_MIRROR $DEBIAN_CODENAME/updates main" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y \
        build-essential libncurses5-dev gawk git subversion libssl-dev gettext zlib1g-dev swig unzip time \
        ccache bzip2 wget sudo file python \
 && apt-get remove -y \
        manpages manpages-dev \
        krb5-locales locales \
 && apt-get -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && useradd -u 1000 -g 100 -m openwrt \
 && echo 'openwrt ALL=NOPASSWD: ALL' > /etc/sudoers.d/openwrt \
 && sudo -iu openwrt mkdir /home/openwrt/sdk

USER openwrt
WORKDIR /home/openwrt/sdk
CMD ["/bin/bash"]
