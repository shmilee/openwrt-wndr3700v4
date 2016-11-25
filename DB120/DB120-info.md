硬件信息
========
主芯片为最新的BCM6358，
交换芯片为BCM5325，
无线芯片为BCM4318，
FLASH容量为16MB，
内存容量为32MB

10.03.1
=======

http://downloads.openwrt.org/backfire/10.03.1/brcm63xx/openwrt-RG100A_DB120-squashfs-cfe.bin
packages: xl2tpd bash


14.07
======
https://downloads.openwrt.org/barrier_breaker/14.07/brcm63xx/generic/openwrt-RG100A_DB120-squashfs-cfe.bin
md5sum: 7533024198f3a1c5fb59a78635d0e6c5

packages:
    * luci-i18n-chinese
    * vpn: xl2tpd ip kmod-l2tp kmod-pppol2tp ppp-mod-pppol2tp resolveip
    * shadow: shadow-common shadow-su shadow-useradd
    * openssh: openssh-client autossh openssh-keygen openssh-server ss

backup:
    * users: root; shmilee;
    * connect: vpnid,vpnpasswd; Openwrt,wuxianmima;
    * ip addr; route; static ip
    * ssh keys for shmilee,root; firewall for ZJU input; wan RootLogin no, login passwd no, only key; autossh -D 3691 script
    * uhttp port 80 --> 180 ;

刷机流程
========

1. 网页刷. 图钉按RST后开电源,等待power红灯后松开.

网线接LAN4,电脑ip设定192.168.1.100,然后网页进入192.168.1.1进行刷机.

2. 重启后, 网线接LAN1-3,网页登入,密码默认admin,设定root登陆密码.

scp上传安装的ipks,利用脚本安装.

网页内恢复备份.
