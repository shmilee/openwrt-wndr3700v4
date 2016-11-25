#/bin/ash

arch='ar71xx'
url='http://openwrt.proxy.ustclug.org/barrier_breaker/14.07/ar71xx/nand/packages'

# 1
chinese_luci="luci/luci-i18n-chinese_0.12+svn-r10530-1_$arch.ipk"

# 6
zjuvpn="base/ip_3.15.0-1_$arch.ipk \
    base/kmod-l2tp_3.10.49-1_$arch.ipk \
    base/kmod-pppol2tp_3.10.49-1_$arch.ipk \
    base/ppp-mod-pppol2tp_2.4.7-2_$arch.ipk \
    base/resolveip_2_$arch.ipk \
    packages/xl2tpd_1.3.6-5619e1771048e74b729804e8602f409af0f3faea_$arch.ipk"

 # 3
shadowusr="packages/shadow-common_4.1.5.1-4_$arch.ipk \
    packages/shadow-su_4.1.5.1-4_$arch.ipk \
    packages/shadow-useradd_4.1.5.1-4_$arch.ipk"


# 5+2
opensshauto="oldpackages/autossh_1.4b-6_$arch.ipk \
    base/libopenssl_1.0.2f-1_$arch.ipk \
    base/zlib_1.2.8-1_$arch.ipk \
    packages/openssh-client_6.6p1-1_$arch.ipk \
    base/ss_3.15.0-1_$arch.ipk"
opensshserver="packages/openssh-keygen_6.6p1-1_$arch.ipk \
    packages/openssh-server_6.6p1-1_$arch.ipk"

# download in PC
read -p "-> download ipks in PC, then exit? [y/n] " ANS0
if [ x$ANS0 == xy ]; then
    [ -d ipks ] && rm -rv ipks
    mkdir -p ipks/{base,luci,oldpackages,packages} #routing,telephony,management}
    for dir in ipks/*; do
        wget -c -O $dir/md5sums $url/$(basename $dir)/md5sums
    done
    > ipks/md5sums
    for ipk in $chinese_luci $zjuvpn $shadowusr $opensshauto $opensshserver; do
        wget -c -O ipks/$ipk $url/$ipk
        sed -n "s|$(basename $ipk)|$ipk|p" \
            ipks/$(dirname $ipk)/md5sums >> ipks/md5sums
    done
    for dir in ipks/*; do
        [ -d $dir ] && rm $dir/md5sums
    done
    cd ipks/
    md5sum -c md5sums
    cd ../
    exit 0
fi

cd ipks/

#check md5sums
if ! md5sum -c md5sums; then
    echo "!!!Some ipks are broken!"
    exit 1
fi

read -p "-> Install luci chinese language? [y/n]" ANS1
if [ x$ANS1 == xy ]; then
    opkg install $chinese_luci
fi

read -p "-> Install ipks for ZJU VPN? [y/n] " ANS2
if [ x$ANS2 == xy ]; then
    opkg install $zjuvpn
fi

read -p "-> Install ipks for cmd useradd and su? [y/n] " ANS3
if [ x$ANS3 == xy ]; then
    opkg install $shadowusr
fi

read -p "-> Install ipks for openssh client? [y/n] " ANS4
if [ x$ANS4 == xy ]; then
    opkg install $opensshauto
    read -p "-> Install ipks for openssh server? [y/n] " ANS5
    if [ x$ANS5 == xy ]; then
        opkg install $opensshserver
    fi
fi

cd ../
echo "==> Done."
