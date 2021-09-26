#!/usr/bin/env sh

# http://www.saschahlusiak.de/linux/isatap.htm#router
# 1. info:
# OpenWrt, WAN6, 2001:da8:X:X:X:X:X:X/64
# OpenWrt, is0, 2001:db8:1234:5:Y:Y::Y/64
# PC, isatapd, is0, 2001:db8:1234:5:Z:Z:Z:Z/64
# 2. test cmd:
# OpenWrt, ping6 ipv6.google.com
#   > PING ipv6.google.com (2404:6800:4008:802::200e): 56 data bytes
#   > 64 bytes from 2404:6800:4008:802::200e: seq=0 ttl=43 time=84.870 ms
# PC, ping OpenWrt-WAN6
#   > 64 bytes from OpenWrt:WAN6: icmp_seq=1 ttl=64 time=0.964 ms
# PC, ping -6 ipv6.google.com
#   > PING ipv6.google.com(tsa03s01-in-x0e.1e100.net (2404:6800:4008:802::200e)) 56 data bytes
#   > From OpenWrt:is0: icmp_seq=1 Destination unreachable: No route # TODO

interface_name='is0'
V4ADDR=`ip addr show eth0.2 | awk '/net /{gsub(/\/\d\d/,"",$2);print$2}'`
PREFIX='2001:db8:1234:5'
radvd_conf='/tmp/radvd.conf'

setup_interface() {
    ip tunnel add $interface_name mode isatap local $V4ADDR ttl 64
    ip link set $interface_name up
    ip addr add $PREFIX::5efe:$V4ADDR/64 dev $interface_name
}

pre_radvd_conf() {
    cat > $radvd_conf <<EOF
interface $interface_name
{
    AdvSendAdvert on;
    UnicastOnly on;
    AdvHomeAgentFlag off;

    prefix $PREFIX::/64
    {
    AdvOnLink on;
    AdvAutonomous on;
    AdvRouterAddr off;
    };
};
EOF
}

setup_isatap_router() {
    setup_interface
    if ip link show $interface_name 2>/dev/null >/dev/null; then
        echo "Success to setup interface $interface_name!"
        pre_radvd_conf
        radvd --config=$radvd_conf --pidfile=/var/run/radvd.pid
    else
        echo "Fail to setup interface $interface_name!"
    fi
}

delete_isatap_router() {
    ip tunnel del $interface_name
    kill `cat /var/run/radvd.pid`
}
if [ x"$1" == "x-s" ]; then
    setup_isatap_router
elif [ x"$1" == "x-d" ]; then
    delete_isatap_router
elif [ x"$1" == "x-r" ]; then
    delete_isatap_router
    setup_isatap_router
else
    echo
    echo "usage: $0 [options]"
    echo "options:"
    echo "  -s  setup ISATAP router"
    echo "  -d  delete ISATAP router"
    echo "  -r  resetup ISATAP router"
    echo
fi
