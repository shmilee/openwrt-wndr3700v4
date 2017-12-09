# debian:jessie-20171009
#
# https://wiki.openwrt.org/doc/howto/buildroot.exigence
# Ignore packages: xz-utils gettext flex
# They can be found in `sdk/staging_dir/host/bin`
#

FROM debian:jessie

LABEL maintainer="shmilee.zju@gmail.com" \
      sdk.version="15.05.1" \
      description="Debian 8 with OpenWRT SDK dependencies"

ENV TIMEZONE=Asia/Shanghai \
    DEBIAN_MIRROR=http://mirrors.163.com/debian \
    DEBIAN_SECURITY_MIRROR=http://mirrors.163.com/debian-security \
    PATH=/home/openwrt/sdk/staging_dir/host/bin:$PATH \
    LD_LIBRARY_PATH=/home/openwrt/sdk/staging_dir/host/lib:$LD_LIBRARY_PATH

COPY dpkg.cfg.excludes /etc/dpkg/dpkg.cfg.d/01_excludes

RUN echo "$TIMEZONE" > /etc/timezone \
 && echo "deb $DEBIAN_MIRROR jessie main" > /etc/apt/sources.list \
 && echo "deb $DEBIAN_MIRROR jessie-updates main" >> /etc/apt/sources.list \
 && echo "deb $DEBIAN_SECURITY_MIRROR jessie/updates main" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y \
        git-core subversion \
        build-essential ccache \
        libssl-dev libncurses5-dev zlib1g-dev \
        unzip bzip2 \
        wget sudo gawk file python \
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
