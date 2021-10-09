# -*- coding: utf-8 -*-

outdir = '../myfiles-example'
templatedir = '.' # template dir
private = '192.168.1.1' # for lan

# str, "string"
# tuple, ('filepath in templatedir', ('replace old', 'new'), ('old', 'new'))
# tuple, (':SUB:', ('replace old', 'new'), ('old', 'new'))

all_myfiles = {

    'etc/config/dhcp': [
        ('etc-config/dhcp', ('192.168.1.1', private)),
        """
config host
	option ip '%s.100'
        option mac '00:11:22:33:44:55'
	option name 'PC-eth0'
""" % private[:-2],
    ],

    'etc/config/dropbear': [
        ('etc-config/dropbear', ('{WANPORT}', '2333')),
    ],

    'etc/config/firewall': [('etc-config/firewall',)],
    'etc/config/fstab': [('etc-config/fstab',)],
    'etc/config/luci': [('etc-config/luci',)],

    'etc/config/network': [
        ('etc-config/network',
            ('192.168.1.1', private),
            ("\nconfig interface 'wan'\n\toption ifname 'eth0.2'\n\toption proto 'dhcp'\n", ""),),
        ('wan-static/etc_config_network',
            ('{IPADDR}', 'xxx.yyy.aa.bb'),
            ('{NETMASK}', '255.255.255.0'),
            ('{GATEWAY}', 'xxx.yyy.aa.1'),
            ('{BROADCAST}', 'xxx.yyy.aa.255'),
            ('{MACADDR}', '11:22:33:44:55:66'),),
    ],

    'etc/config/system': [('etc-config/system',)],

    'etc/config/wireless': [
        ('etc-config/wireless',
            ('{SSID}', 'OpenWrt2.4G'),
            ('{WIFIKEY}', 'wifipasswd'),),
    ],

    'etc/opkg/distfeeds.conf': [
        ('etc/opkg_distfeeds.conf',
            ('http://downloads.openwrt.org/',
            'https://openwrt.proxy.ustclug.org/')),
    ],

    'etc/shadow': [
        ('etc/shadow', 
            ('root::0:0:99999:7:::',
            'root:$1$sPPrXFMR$8whltV2NanMOQoosnALYg0:17149:0:99999:7:::')),
        # `openssl passwd -1 12345678`
        # -1 MD5-based password algorithm
    ],

}

# enable ZJU VPN
all_myfiles['etc/config/network'].extend([
    ('zjuvpn-static-routes/etc_config_network',
        ('{USER}', 'vpnid@a'),
        ('{PASSWD}', 'vpnpassword')),
    ('zjuvpn-static-routes/yq-routes',
        ('{WANGATEWAY}', 'xxx.yyy.aa.1')),
])

all_myfiles['etc/config/firewall'].extend([
    (':SUB:', ("\tlist   network\t\t'wan'\n\tlist   network\t\t'wan6'",
               "\tlist   network\t\t'wan'\n\tlist   network\t\t'wan6'\n\tlist   network\t\t'zjuvpn'")),
])

# enable 5G WiFi
all_myfiles['etc/config/wireless'].extend([
    ('wifi-5g/etc_config_wireless',
        ("""
	# REMOVE THIS LINE TO ENABLE WIFI:
	option disabled 1""", ''),
        ('{SSID}', 'OpenWrt5G'),
        ('{WIFIKEY}', '5gwifipasswd'),),
])

# enable guest 2.4G WiFi
all_myfiles['etc/config/wireless'].extend([
    ('wifi-guest/etc_config_wireless',
        ('{SSID}', 'Guest'),
        ('{WIFIKEY}', 'guestpassword'),),
])

all_myfiles['etc/config/network'].extend([
    ('wifi-guest/etc_config_network',
        ('{IPADDR}', '192.168.6.1'),),
])

all_myfiles['etc/config/dhcp'].extend([
    ('wifi-guest/etc_config_dhcp',
        ('{DHCPOption}', '6,192.168.6.1'),
        ('{LeaseTime}', '6h'),),
])

all_myfiles['etc/config/firewall'].extend([
    ('wifi-guest/etc_config_firewall',
        ('192.168.1.1', private),),
])
