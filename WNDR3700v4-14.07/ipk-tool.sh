#/bin/ash

arch='ar71xx'
mirror='../mirror-tools/openwrt-ipks-14.07/ar71xx/nand/packages'

chinese_luci="luci/luci-i18n-chinese_0.12+svn-r10530-1_$arch.ipk"
zjuvpn="base/ip_3.15.0-1_$arch.ipk \
    base/kmod-l2tp_3.10.49-1_$arch.ipk \
    base/kmod-pppol2tp_3.10.49-1_$arch.ipk \
    base/ppp-mod-pppol2tp_2.4.7-2_$arch.ipk \
    base/resolveip_2_$arch.ipk \
    packages/xl2tpd_1.3.6-5619e1771048e74b729804e8602f409af0f3faea_$arch.ipk"
shadowusr="packages/shadow-common_4.1.5.1-4_$arch.ipk \
    packages/shadow-su_4.1.5.1-4_$arch.ipk \
    packages/shadow-useradd_4.1.5.1-4_$arch.ipk"
opensshauto="oldpackages/autossh_1.4b-6_$arch.ipk \
    base/libopenssl_1.0.2f-1_$arch.ipk \
    base/zlib_1.2.8-1_$arch.ipk \
    packages/openssh-client_6.6p1-1_$arch.ipk \
    base/ss_3.15.0-1_$arch.ipk"
opensshserver="packages/openssh-keygen_6.6p1-1_$arch.ipk \
    packages/openssh-server_6.6p1-1_$arch.ipk"

ask() {
    read -p "$@ [y/n]" ANS
    [ x$ANS == xy ] && return 0 || return 1
}

# download in PC
if ask "-> download ipks in PC, then exit?"; then
    [ -d ipks ] && rm -rv ipks
    for ipk in $chinese_luci $zjuvpn $shadowusr $opensshauto $opensshserver; do
        install -v -Dm644 $mirror/$ipk ipks/$ipk
    done
    cd ipks/
    find * -type f -exec md5sum {} \; > md5sums
    exit 0
fi

cd ipks/
if ! md5sum -c md5sums; then
    echo "!!!Some ipks are broken!"
    exit 1
fi

if ask "-> Install luci chinese language?"; then
    opkg install $chinese_luci
fi

if ask "-> Install ipks for ZJU VPN?"; then
    opkg install $zjuvpn
fi

if ask "-> Install ipks for cmd useradd and su?"; then
    opkg install $shadowusr
fi

if ask "-> Install ipks for openssh client?"; then
    opkg install $opensshauto
    if ask "-> Install ipks for openssh server?"; then
        opkg install $opensshserver
    fi
fi

cd ../
echo "==> Done."
