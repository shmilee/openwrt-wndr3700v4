# -*- coding: utf-8 -*-

all_templates = """
etc/config/dhcp
etc/config/dropbear
etc/config/firewall
etc/config/luci
etc/config/network
etc/config/system
etc/config/uhttpd
etc/config/wireless
etc/dnsmasq.conf
etc/opkg/distfeeds.conf
"""

# ('ADD', "str"), ('REPLACE', ('old', 'new')),
# ('ADDFILE', 'filepath', ('old', 'new'))

all_myfiles = dict(

    etc_config_dhcp=(
        ('ADD', """
config host
	option ip '192.168.1.100'
        option mac '00:11:22:33:44:55'
	option name 'PC-eth0'
"""),
    ),

    etc_config_dropbear=(
        ('REPLACE', ('{WANPORT}', '2333')),
    ),

    etc_config_firewall=(),
    etc_config_luci=(),

    etc_config_network=(
        ('REPLACE', ('{WANNET}', """
config interface 'wan'
	option ifname 'eth0.2'
	option _orig_ifname 'eth0.2'
	option _orig_bridge 'false'
	option proto 'static'
	option ipaddr 'xxx.yyy.aa.bb'
	option netmask '255.255.255.0'
	option gateway 'xxx.yyy.aa.1'
	option broadcast 'xxx.yyy.aa.255'
	option macaddr '11:22:33:44:55:66'
	option dns '10.10.0.21'
""")),
        ('REPLACE', ('{VPN-ID}', 'idexample')),
        ('REPLACE', ('{VPN-PASSWD}', 'pswdexample')),
        ('ADDFILE', './static-routes/yq-routes',
            ('{WANGATEWAY}', 'xxx.yyy.aa.1')),
    ),
    etc_config_system=(),
    etc_config_uhttpd=(),

    etc_config_wireless=(
        ('REPLACE', ('{SSID}', 'OpenWrt')),
        ('REPLACE', ('{WIFIKEY}', 'wifipasswd')),
    ),

    etc_dnsmasq_d_conf=(
        ('ADD', "address=/shmilee.io/xx.yy.zz.aa\n"),
    ),

    etc_opkg_distfeeds_d_conf=(
        ('REPLACE', ('http://downloads.openwrt.org/chaos_calmer/15.05.1',
                     'http://shmilee.io/repo-shmilee/openwrt-ipks-15.05.1')),
    ),
)
