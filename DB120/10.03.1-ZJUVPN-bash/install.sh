#http://openwrt.proxy.ustclug.org/backfire/10.03.1/brcm63xx/packages/
opkg install libncurses_5.7-2_brcm63xx.ipk bash_4.2-1_brcm63xx.ipk
opkg install xl2tpd_1.3.0-1_brcm63xx.ipk
tar xvf vpn-arch.tar -C /
cat ./firewall.user >>/etc/firewall.user
echo vi /usr/sbin/vpn-connect about xl2tpd
