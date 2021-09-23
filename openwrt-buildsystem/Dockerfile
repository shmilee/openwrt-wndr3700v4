# debian:buster-20210902
# https://openwrt.org/docs/guide-developer/build-system/install-buildsystem

FROM debian:buster

LABEL maintainer="shmilee.zju@gmail.com" \
      sdk.version="19.07.8" \
      description="Debian 10 with OpenWRT build system prerequisites"

ENV TIMEZONE=Asia/Shanghai \
    DEBIAN_CODENAME=buster \
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
        build-essential ccache ecj fastjar file g++ gawk \
        gettext git java-propose-classpath libelf-dev libncurses5-dev \
        libncursesw5-dev libssl-dev python python2.7-dev python3 unzip wget \
        python3-distutils python3-setuptools python3-dev rsync subversion \
        swig time xsltproc zlib1g-dev \
        bzip2 sudo \
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
