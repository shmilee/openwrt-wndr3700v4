WNDR3700v4 Information
======================

```shell
$ cat /proc/cpuinfo 
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

$ head -n1 /proc/meminfo
MemTotal:         126020 kB
```

WNDR3700v4-15.05.1
==================

固件: 按 [WNDR3700v4-15.05.1/readme.md](WNDR3700v4-15.05.1/readme.md) 编译,
当前版本 `openwrt-15.05.1-ar71xx-nand-wndr3700v4-ubi-factory-20161204-with-myfiles.img`.
MD5(f8621dee92836a2cadedfeffaa725dde)

Installation via serial console and TFTP
========================================

Reset, 电源灯长闪绿灯后,

```shell
[$] tftp 192.168.1.1
tftp> mode binary
tftp> put openwrt-15.05.1-ar71xx-nand-wndr3700v4-ubi-factory-20161204-with-myfiles.img
tftp> quit
```

后续
=====

* 首次登录 http://192.168.1.1:180/cgi-bin/luci 后，设置 root 密码。

* 禁用暂时不用的启动项 telnet, shadowsocks, ddns, adbyby

* 添加 user shmilee

```shell
useradd -d /etc/shmilee -m -s /bin/ash shmilee
passwd shmilee
mkdir /etc/shmilee/.ssh
```

* 添加电脑的SSH公共密钥到 `/etc/dropbear/authorized_keys`.  
  shmilee 登录需要 `/etc/shmilee/.ssh/authorized_keys`

* wan ssh登录, 需确保防火墙入站数据为接受 `option input 'ACCEPT'`

* 为 `autossh -D 3696` 生成一对密钥, 放在 `/etc/shmilee/.ssh/`.  
  公钥添加到3690对应的主机. 手动登录一次, 以生成 `/root/.ssh/known_hosts`.

* 恢复 nginx 配置, `nginx-frontend.conf`, `ssl-certs/`.
