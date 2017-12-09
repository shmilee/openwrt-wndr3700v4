#/bin/sh
# Copyright (C) 2016 shmilee

. /etc/6in4-server.conf
WANIP=`ip -4 addr show dev $WANIF | awk '/inet / {print $2}' | cut -d/ -f1`
TUNGW=`ip -6 addr show dev $WANIF| awk '/inet6 fe80/ {print $2}'|cut -d/ -f1`

setup6in4() {
    ip tunnel add $TUNIF mode sit local $WANIP remote any
    ip link set $TUNIF mtu $TUNMTU
    ip addr add $TUNPREFIX::1/64 dev $TUNIF
    ip link set $TUNIF up
    ip route del $TUNPREFIX::/64 dev $TUNIF
    ip route add $TUNPREFIX::/64 via $TUNGW dev $TUNIF
    if ifconfig | grep $TUNIF > /dev/null; then
        echo "Success to set up 6in4 Tunnel Server!"
    else
        echo "Fail to set up 6in4 Tunnel Server!"
    fi
}

if [ $# -lt 1 ]; then
    setup6in4
elif [ "$1" == "-d" ]; then
    ip tunnel del $TUNIF
else
    echo "Usage: ipv6    : Set up 6in4 Tunnel Server"
    echo "       ipv6 -d : delete 6in4 Tunnel Server"
fi
