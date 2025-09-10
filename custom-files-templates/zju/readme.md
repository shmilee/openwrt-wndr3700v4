## wan 静态 IP

* `wan-static-network` 替换 `{XXX}` 后，添加至 `etc/config/network`.

## VPN

* `vpn-network` 替换 `{XXX}` 后，添加至 `etc/config/network`.

* `etc/config/firewall` zone wan 中添加 `list network 'zjuvpn'`

## 静态路由

[新版客户端](http://zuits.zju.edu.cn/redir.php?catalog_id=1921&object_id=1935)
[016.04.14](http://zuits.zju.edu.cn/wescms/sys/filebrowser/file.php?cmd=download&id=391112)

FILE: DoubleLineRouteMgr.ini

```
0=10.0.0.0/8
1=210.32.0.0/20
2=222.205.0.0/17
3=210.32.128.0/19
4=210.32.160.0/21
5=210.32.168.0/22
6=210.32.172.0/23
7=210.32.174.0/24
8=210.32.176.0/20
9=58.196.192.0/19
10=58.196.224.0/20
```

* `yq-routes` 或 `zjg-routes`，替换 gateway 后，添加至 `etc/config/network`.
