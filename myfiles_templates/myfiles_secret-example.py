# -*- coding: utf-8 -*-

outdir = '../myfiles_for_image'
templatedir = '.'

all_templates = """
etc/config/dhcp
etc/config/dropbear
etc/config/firewall
etc/config/fstab
etc/config/hd-idle
etc/config/luci
etc/config/network
etc/config/system
etc/config/uhttpd
etc/config/wireless
etc/dnsmasq.conf
etc/opkg/distfeeds.conf
etc/shadow
"""

# ('ADD', "str"), ('REPLACE', ('old', 'new'), ('old', 'new')),
# ('ADDFILE', 'filepath', ('old', 'new'), ('old', 'new'))

all_myfiles = {

    'etc/config/dhcp': [
        ('ADD', """
config host
	option ip '192.168.1.100'
        option mac '00:11:22:33:44:55'
	option name 'PC-eth0'
"""),
    ],

    'etc/config/dropbear': [
        ('REPLACE', ('{WANPORT}', '2333')),
    ],

    'etc/config/firewall': [],
    'etc/config/fstab': [],
    'etc/config/hd-idle': [],
    'etc/config/luci': [],

    'etc/config/network': [
        ('REPLACE', ('{IPADDR}', 'xxx.yyy.aa.bb'),
         ('{NETMASK}', '255.255.255.0'),
         ('{GATEWAY}', 'xxx.yyy.aa.1'),
         ('{BROADCAST}', 'xxx.yyy.aa.255'),
         ('{MACADDR}', '11:22:33:44:55:66'),),
    ],

    'etc/config/system': [],
    'etc/config/uhttpd': [],

    'etc/config/wireless': [
        ('REPLACE', ('{SSID}', 'OpenWrt2.4G'),
         ('{WIFIKEY}', 'wifipasswd'),),
    ],

    'etc/dnsmasq.conf': [
        ('ADD', "address=/pcbeta.com/218.93.127.136\n"),
    ],

    'etc/opkg/distfeeds.conf': [
        ('REPLACE', ('http://downloads.openwrt.org/',
                     'http://openwrt.proxy.ustclug.org/')),
    ],

    'etc/shadow': [
        ('REPLACE', ('root::0:0:99999:7:::',
                     'root:$1$sPPrXFMR$8whltV2NanMOQoosnALYg0:' +
                     '17149:0:99999:7:::')),
        # `openssl passwd -1 12345678`
        # -1 MD5-based password algorithm
    ],

}

# enable ZJU VPN
all_myfiles['etc/config/network'].extend([
    ('ADD', """
config interface 'zjuvpn'
	option proto 'l2tp'
	option server '10.5.1.9'
	option username 'vpnid@a'
	option password 'vpnpassword'
	option mtu '1428'

"""),
    ('ADDFILE', templatedir + '/static-routes/yq-routes',
        ('{WANGATEWAY}', 'xxx.yyy.aa.1')),
])

all_myfiles['etc/config/firewall'].extend([
    ('REPLACE', ("\tlist   network\t\t'wan'\n\tlist   network\t\t'wan6'",
                 "\tlist   network\t\t'wan'\n\tlist   network\t\t'wan6'\n\tlist   network\t\t'zjuvpn'")),
])

# enable 5G WiFi
all_myfiles['etc/config/wireless'].extend([
    ('ADDFILE', templatedir + '/wifi-5g/etc_config_wireless',
        ("""
	# REMOVE THIS LINE TO ENABLE WIFI:
	option disabled 1""", ''),
        ('{SSID}', 'OpenWrt5G'),
        ('{WIFIKEY}', '5gwifipasswd'),),
])

# enable guest 2.4G WiFi
all_myfiles['etc/config/wireless'].extend([
    ('ADDFILE', templatedir + '/wifi-guest/etc_config_wireless',
        ('{SSID}', 'Guest'),
        ('{WIFIKEY}', 'guestpassword'),),
])

all_myfiles['etc/config/network'].extend([
    ('ADDFILE', templatedir + '/wifi-guest/etc_config_network',
        ('{IPADDR}', '192.168.6.1')),
])

all_myfiles['etc/config/dhcp'].extend([
    ('ADDFILE', templatedir + '/wifi-guest/etc_config_dhcp',
        ('{DHCPOption}', '6,192.168.6.1'),
        ('{LeaseTime}', '6h'),),
])

all_myfiles['etc/config/firewall'].extend([
    ('ADDFILE', templatedir + '/wifi-guest/etc_config_firewall'),
])
