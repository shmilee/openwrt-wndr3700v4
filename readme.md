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

固件: 按 [build_myimage.md](./build_myimage.md) 编译,
版本命名 `openwrt-xx.xx.x-ath79-nand-netgear_wndr3700-v4-squashfs-factory-20YYmmdd-with-myfiles.img`.

当前采用版本 `openwrt-14.10.2`。

Installation via serial console and TFTP
========================================

LAN 口连接网线，电脑 IP 设为 `192.168.1.100/24` 后，reset 路由，直至电源灯由 **橙色闪烁** 变到 **绿色闪烁**。

```shell
[$] ping 192.168.1.1
[$] tftp 192.168.1.1
tftp> mode binary
tftp> put openwrt-xx.xx.x-ar71xx-nand-wndr3700v4-ubi-factory-20YYmmdd-with-myfiles.img
tftp> quit
```

后续
=====

* 登录 http://192.168.37.1:180/
    - 系统 > 系统 > 系统属性 > 常规设置 > **同步浏览器时间**
    - 系统 > 管理权 > 路由器密码 > 更改 root 密码
    - 系统 > 启动项 > 启动脚本 > 禁用暂时不用的启动项：ddns, transmission

* 5G启用，必须 **断电重启** 一次。

* 终端登陆 `ssh root@192.168.37.1`
    - FIX: LAN 无法获取 ipv6 地址，修改 `/etc/config/dhcp`，server to hybrid
      ```
      config dhcp 'lan'  
            ......
            option dhcpv6 'hybrid'
            option ra 'hybrid'
      ```
    - [ZJU 静态 IP、VPN 账号密码和静态路由等](custom-files-templates/zju/readme.md)
    - 用户 openwrt 家目录权限
      ```
      root@OpenWrt:~# chown -R 1000:100 /home/openwrt/
      ```
    - 添加电脑 SSH 公钥
      ```shell
      ssh-copy-id root@192.168.37.1
      ssh-copy-id openwrt@192.168.37.1
      ```
    - USB 外接硬盘, (电脑上格式化为 ext4, 卷标 RouterUSB: `mkfs.ext4 -L 'RouterUSB' /dev/sdXX`)。  
      路由中添加目录：
      ```shell
      root@OpenWrt:~# mkdir -p /mnt/sda1/aria2
      root@OpenWrt:~# chown -R aria2:aria2 /mnt/sda1/aria2
      root@OpenWrt:~# mkdir -p /mnt/sda1/transmission
      root@OpenWrt:~# chown -R transmission:transmission /mnt/sda1/transmission
      ```

* 网络 > 无线 > radio1 > 扫描，加入网络
    - 网络名称：wwan
    - 防火墙区域：wan wan6
    - 密码：xxx

* 添加 swap
    - 创建 swap 文件
      ```
      root@OpenWrt:~# dd if=/dev/zero of=/mnt/sda1/swap bs=1024 count=256000
      root@OpenWrt:~# mkswap /mnt/sda1/swap
      root@OpenWrt:~# swapon /mnt/sda1/swap
      ```
    - /etc/config/fstab 中增加
      ```
      config swap
      	option enabled '1'
      	option device '/mnt/sda1/swap'
      ```

* 添加 tailscale。准备好 `headscale apikeys create`
  ```
  root@OpenWrt:~# opkg update
  root@OpenWrt:~# opkg install tailscale
  root@OpenWrt:~# tailscale up \
    --login-server https://headscale.your-server.domain \
    --accept-routes=true --accept-dns=false \
    --advertise-routes=10.0.0.0/8 \
    --auth-key your-apikey-xxxxxx
  ```

