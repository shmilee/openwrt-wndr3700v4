#/bin/ash

chinese_luci="luci-i18n-chinese_0.12+svn-r10530-1_brcm63xx.ipk"
# 6
zjuvpn="ip_3.15.0-1_brcm63xx.ipk \
    kmod-l2tp_3.10.49-1_brcm63xx.ipk \
    kmod-pppol2tp_3.10.49-1_brcm63xx.ipk \
    ppp-mod-pppol2tp_2.4.7-2_brcm63xx.ipk \
    resolveip_2_brcm63xx.ipk \
    xl2tpd_1.3.6-5619e1771048e74b729804e8602f409af0f3faea_brcm63xx.ipk"
# 3
shadowusr="shadow-common_4.1.5.1-4_brcm63xx.ipk \
    shadow-su_4.1.5.1-4_brcm63xx.ipk \
    shadow-useradd_4.1.5.1-4_brcm63xx.ipk"
# 5+2
opensshauto="autossh_1.4b-6_brcm63xx.ipk \
    libopenssl_1.0.1j-1_brcm63xx.ipk \
    zlib_1.2.8-1_brcm63xx.ipk \
    openssh-client_6.6p1-1_brcm63xx.ipk \
    ss_3.15.0-1_brcm63xx.ipk"
opensshserver="openssh-keygen_6.6p1-1_brcm63xx.ipk \
    openssh-server_6.6p1-1_brcm63xx.ipk"

#check md5sums
if ! md5sum -c md5sums; then
    echo "!!!Some ipks are broken!"
    exit 1
fi

echo "-> Install luci chinese language."
opkg install $chinese_luci

read -p "-> Install ipks for ZJU VPN? [y/n] " ANS1
if [ x$ANS1 == xy ]; then
    opkg install $zjuvpn
fi

read -p "-> Install ipks for cmd useradd and su? [y/n] " ANS2
if [ x$ANS2 == xy ]; then
    opkg install $shadowusr
fi

read -p "-> Install ipks for openssh client? [y/n] " ANS3
if [ x$ANS3 == xy ]; then
    opkg install $opensshauto
    read -p "-> Install ipks for openssh server? [y/n] " ANS4
    if [ x$ANS4 == xy ]; then
        opkg install $opensshserver
    fi
fi

echo "==> Done."
