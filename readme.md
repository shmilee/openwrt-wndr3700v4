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

WNDR3700v4 Image
==================

NOTE:
   1. note for [trouble upgrade from 19.07 to 21.02](https://forum.openwrt.org/t/trouble-upgrading-netgear-wndr-4300v1-from-19-07-to-21-02/106823), **recommend flashing factory images**!
   2. 当前版本 [v20211009](https://github.com/shmilee/openwrt-wndr3700v4/releases/tag/v20211009), 采用的是 openwrt-19.07.8。
   3. master 分支 TODO: openwrt-21.02 check `openwrt/target/linux/ath79/dts/ar9344_netgear_wndr.dtsi`, 128M

固件: 按 [build_myimage.md](./build_myimage.md) 编译,
版本命名 `openwrt-xx.xx.x-ar71xx-nand-wndr3700v4-ubi-factory-2yyymmdd-with-myfiles.img`.

Installation via serial console and TFTP
========================================

Reset, 直到电源灯由 **橙色闪烁** 变到 **绿色闪烁**.

```shell
[$] tftp 192.168.1.1
tftp> mode binary
tftp> put openwrt-xx.xx.x-ar71xx-nand-wndr3700v4-ubi-factory-2yyymmdd-with-myfiles.img
tftp> quit
```

后续
=====

* ~~首次登录 http://192.168.1.1:180/cgi-bin/luci 后，设置 root 密码。~~

* 更换 zjuvpn 密码, `'/etc/config/network'`, `config interface 'zjuvpn'`

* FIX: 连接 zjuvpn 后, LAN 无法访问外网, 原因是 `adbyby` 添加的防火墙

  `/etc/config/firewall`
  ```
  #config include 'adbyby'
  #       option type 'script'
  #       option path '/usr/share/adbyby/firewall.include'
  #       option reload '1' 
  ```

* FIX: LAN 无法获取校园 ipv6 地址

  `/etc/config/dhcp`
  ```
  config dhcp 'lan'  
        ......
        option dhcpv6 'hybrid'
        option ra 'hybrid'
  ```

* 5G启用，必须 **断电重启** 一次。

* 禁用暂时不用的启动项 shadowsocks, ddns, transmission

* ~~添加 user shmilee~~

* 添加电脑的SSH公共密钥到 `/etc/dropbear/authorized_keys`.  
  shmilee 登录需要 `/etc/shmilee/.ssh/authorized_keys`

* ~~wan ssh登录, 需确保防火墙入站数据为接受 `option input 'ACCEPT'`~~

* 为 `autossh -D 3696` 生成一对密钥, 放在 `/etc/shmilee/.ssh/`.  
  公钥添加到3690对应的主机. 手动登录一次, 以生成 `/root/.ssh/known_hosts`.

* 恢复 nginx 配置, `nginx-frontend.conf`, `ssl-certs/`.

* USB外接硬盘, 格式化为 `ext4`, 卷标 `RouterUSB`.

```shell
mkdir -p /etc/shmilee/.aria2
mkdir -p /mnt/sda1
chown shmilee:users -R /etc/shmilee/
chown shmilee:users -R /mnt/sda1
smbpasswd -a shmilee
```

