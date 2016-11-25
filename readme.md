Information
============

```shell
# cat /proc/cpuinfo 
system type		: Atheros AR9344 rev 2
machine			: NETGEAR WNDR3700v4
processor		: 0
cpu model		: MIPS 74Kc V4.12
BogoMIPS		: 278.93
wait instruction	: yes
microsecond timers	: yes
tlb_entries		: 32
extra interrupt vector	: yes
hardware watchpoint	: yes, count: 4, address/irw mask: [0x0000, 0x0ff8, 0x0ff8, 0x0ff8]
isa			: mips1 mips2 mips32r1 mips32r2
ASEs implemented	: mips16 dsp dsp2
shadow register sets	: 1
kscratch registers	: 0
core			: 0
VCED exceptions		: not available
VCEI exceptions		: not available

# head -n1 /proc/meminfo
MemTotal:         126020 kB
```

14.07
======

http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/nand/openwrt-ar71xx-nand-wndr3700v4-ubi-factory.img

md5sum:0137f3e3a865434cfff5e2578e5abab4

packages:

    * luci-i18n-chinese
    * vpn: xl2tpd ip kmod-l2tp kmod-pppol2tp ppp-mod-pppol2tp resolveip
    * shadow: shadow-common shadow-su shadow-useradd
    * openssh: openssh-client autossh openssh-keygen openssh-server ss

backup:

    * users: root; shmilee;
    * connect: vpnid,vpnpasswd; Openwrt,ssidpasswd;
    * ip addr; route; static ip;
    * ssh keys for shmilee,root; firewall for ZJU input; wan RootLogin no, login passwd no, only key; autossh -D 3691 script;
    * uhttp port 80 --> 180;

About route:

```shell
config route
	option interface 'wan'
	option target '10.0.0.0'
	option netmask '255.0.0.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.0.0'
	option netmask '255.255.240.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '222.205.0.0'
	option netmask '255.255.128.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.128.0'
	option netmask '255.255.224.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.160.0'
	option netmask '255.255.248.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.168.0'
	option netmask '255.255.252.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.172.0'
	option netmask '255.255.254.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '210.32.176.0'
	option netmask '255.255.240.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '58.196.192.0'
	option netmask '255.255.224.0'
	option gateway 'xxx.xxx.xxx.xxx'

config route
	option interface 'wan'
	option target '58.196.224.0'
	option netmask '255.255.240.0'
	option gateway 'xxx.xxx.xxx.xxx'
```

installation via serial console and TFTP
========================================

```shell
tftp> tftp 192.168.1.1
tftp> mode binary
tftp> put openwrt-ar71xx-generic-wndr3700XXX-squashfs-factory.img
tftp> quit
```

TODO full 128M
===============

https://wiki.openwrt.org/doc/techref/flash.layout
https://dev.openwrt.org/changeset/48456/trunk
http://blog.sina.com.cn/s/blog_5f66526e0102wfzo.html
http://www.right.com.cn/forum/thread-144853-1-1.html
