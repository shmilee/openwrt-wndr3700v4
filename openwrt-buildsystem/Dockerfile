# https://www.debian.org/releases/
#   bookworm, 2023.06, python-3.11
# https://hub.docker.com/_/debian
#   debian:bookworm-20250811, 12.11
# https://openwrt.org/docs/guide-developer/build-system/install-buildsystem

FROM debian:bookworm-20250811

LABEL maintainer="shmilee.zju@gmail.com" \
      sdk.version="24.10.x" \
      description="Debian 12 with OpenWRT build system prerequisites"

ENV TIMEZONE=Asia/Shanghai \
    DEBIAN_CODENAME=bookworm \
    DEBIAN_MIRROR=mirrors.ustc.edu.cn

COPY dpkg.cfg.excludes /etc/dpkg/dpkg.cfg.d/01_excludes

RUN echo "$TIMEZONE" > /etc/timezone \
 && sed -i "s/deb.debian.org/$DEBIAN_MIRROR/g" /etc/apt/sources.list.d/debian.sources \
 && apt-get update \
 && apt-get install -y \
    build-essential clang flex bison g++ gawk \
    gcc-multilib g++-multilib gettext git libncurses5-dev libssl-dev \
    python3-setuptools rsync swig unzip zlib1g-dev file wget \
    python3-distutils bzip2 sudo \
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
