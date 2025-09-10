# -*- coding: utf-8 -*-

outdir = '../myfiles_for_image'
templatedir = '.'  # template dir

aria2token = 't/WWPJcgxQjqtTdFCxrE12vpjDlx6v9v7hlD'  # openssl rand -base64 27
lan198ip = '192.168.37.1'  # for lan, xx.yy.zz.1
sshwanport = '2234'
wifi2g = 'Wrt2.4G'
wifi2gkey = '3700v4wifipassword'
wifi5g = 'Wrt5G'
wifi5gkey = '3700v4wifi5gpasswd'
mirror = 'openwrt.proxy.ustclug.org'
# openssl passwd -5 123456789isbad
#   -5  SHA256-based password algorithm
rootpass = '$5$vG4V0wYQV7AarfB2$/JNtzWflcW5ZftyBvptYPgOLgZ77/BicYR8Km2guK67'
guestlanip = '192.168.66.1'  # for guest, aa.bb.cc.1
guest2g = 'Guest2.4G'
guest2gkey = '3700v4wifi2gguest'

# str, "string"
# tuple, ('filepath in templatedir', ('replace old', 'new'), ('old', 'new'))
# tuple, (':SUB:', ('replace old', 'new'), ('old', 'new'))

all_myfiles = {

    'etc/config/aria2': [
        ('etc/config/aria2', ('{TOKEN}', aria2token)),
    ],

    'etc/config/dhcp': [
        ('etc/config/dhcp', ('192.168.1.1', lan198ip)),
    ],

    'etc/config/dropbear': [
        ('etc/config/dropbear', ('{WANPORT}', sshwanport)),
    ],

    'etc/config/firewall': [('etc/config/firewall',)],
    'etc/config/fstab': [('etc/config/fstab',)],
    'etc/config/hd-idle': [('etc/config/hd-idle',)],
    'etc/config/luci': [('etc/config/luci',)],

    'etc/config/network': [
        ('etc/config/network', ('192.168.1.1', lan198ip)),
    ],

    'etc/config/nfs': [
        ('etc/config/nfs', ('192.168.1.0', lan198ip[:-1]+'0')),
    ],

    'etc/config/system': [('etc/config/system',)],
    'etc/config/uhttpd': [('etc/config/uhttpd',)],

    'etc/config/wireless': [
        ('etc/config/wireless', ('{SSID}', wifi2g), ('{WIFIKEY}', wifi2gkey)),
    ],

    'etc/opkg/distfeeds.conf': [
        ('etc/opkg/distfeeds.conf', ('downloads.openwrt.org', mirror)),
    ],

    'etc/uci-defaults/10_disable_services': [
        ('etc/uci-defaults/10_disable_services',)
    ],

    'etc/dnsmasq.conf': [('etc/dnsmasq.conf',)],
    'etc/passwd': [('etc/passwd',)],

    'etc/shadow': [
        ('etc/shadow',
            ('root:::0:99999:7:::', 'root:%s:17149:0:99999:7:::' % rootpass)
         ),
    ],
}

# enable 5G WiFi
all_myfiles['etc/config/wireless'].extend([
    ('wifi-5g/etc_config_wireless',
        ("""
	# REMOVE THIS LINE TO ENABLE WIFI:
	option disabled 1""", ''),
        ('{SSID}', wifi5g),
        ('{WIFIKEY}', wifi5gkey),
     ),
])

# enable guest 2.4G WiFi
all_myfiles['etc/config/dhcp'].extend([
    ('wifi-guest/etc_config_dhcp',
        ('{DHCPOption}', '6,%s' % guestlanip),
        ('{LeaseTime}', '6h'),
     ),
])

all_myfiles['etc/config/firewall'].extend([
    ('wifi-guest/etc_config_firewall', ('192.168.1.1', lan198ip)),
])

all_myfiles['etc/config/network'].extend([
    ('wifi-guest/etc_config_network',
        ('{IPADDR}', guestlanip),
        ('192.168.1.1', lan198ip),
     ),
])

all_myfiles['etc/config/wireless'].extend([
    ('wifi-guest/etc_config_wireless',
        ('{SSID}', guest2g),
        ('{WIFIKEY}', guest2gkey),
     ),
])

# optional: client fixed IP
lapwlan0mac = '66:55:11:ee:88:33'
all_myfiles['etc/config/dhcp'].extend([
    """
config host
	option ip '%s.100'
	option mac %s
	option name 'laptop-wlan0'
""" % (lan198ip[:-2], lapwlan0mac),
])

# optional: ZJU, wan dhcp -> static
zjuip = '222.205.55.16'
zjumac = '11:22:33:44:55:66'
zjuiprefix = '.'.join(zjuip.split('.')[:3])
all_myfiles['etc/config/network'].extend([
    # delete dhcp
    (':SUB:', (
        "\nconfig interface 'wan'\n\toption device 'eth0.2'\n\toption proto 'dhcp'\n",
        ""),
     ),
    # add static
    ('zju/wan-static-network',
        ('{IPADDR}', zjuip),
        ('{NETMASK}', '255.255.255.0'),
        ('{GATEWAY}', '%s.1' % zjuiprefix),
        ('{BROADCAST}', '%s.255' % zjuiprefix),
        ('{MACADDR}', zjumac),
     ),
])

# optional: ZJU, dns
all_myfiles['etc/dnsmasq.conf'].extend([
    'server=10.10.0.21\n\n',
])

# optional: ZJU, VPN + static routes
vpnuser = 'vpnid@abcd'
vpnpass = '设置vpn-password'
fwmatch = "\tlist   network\t\t'wan'\n\tlist   network\t\t'wan6'"  # firewall
all_myfiles['etc/config/network'].extend([
    ('zju/vpn-network', ('{USER}', vpnuser), ('{PASSWD}', vpnpass)),
    ('zju/zjg-routes', ('{WANGATEWAY}', '%s.1' % zjuiprefix)),  # routes
])
all_myfiles['etc/config/firewall'].extend([
    (':SUB:', (fwmatch, fwmatch + "\n\tlist   network\t\t'zjuvpn'")),
])

# optional: creates a new user account
username = 'openwrt'
# openssl passwd -5 "3700v1234's_key"
userpass = '$5$FeiWKosKvbyTQfN2$geOat06yO.05s9IqRGGUEYbHevLrnAFDC7jeHogJwe4'
all_myfiles['etc/passwd'].extend([
    "%s:x:1000:100::/home/%s:/bin/ash\n" % (username, username),
])
all_myfiles['etc/shadow'].extend([
    "%s:%s:17149:0:99999:7:::\n" % (username, userpass),
])
all_myfiles['home/%s/.ssh/authorized_keys' % username] = ['']  # empty
