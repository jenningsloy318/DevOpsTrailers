## Configure XRDP on ubuntu-mate 18.04
1. install package 
```
apt install xrdp xorgxrdp -y
 
```

2. create new startubuntu.sh 
```
if [ ! -e /etc/xrdp/startubuntu.sh ] ; then
cat >> /etc/xrdp/startubuntu.sh << EOF
#!/bin/sh
export XDG_CURRENT_DESKTOP=MATE
exec /etc/xrdp/startwm.sh
EOF
chmod a+x /etc/xrdp/startubuntu.sh
fi
```

3. modify config 
```
sed -i_orig -e 's/startwm/startubuntu/g' /etc/xrdp/sesman.ini
sed -i 's/^TerminalServerUsers/#TerminalServerUsers/g' /etc/xrdp/sesman.ini
sed -i 's/^TerminalServerAdmins/#TerminalServerAdmins/g' /etc/xrdp/sesman.ini
sed -i_orig -e 's/allowed_users=console/allowed_users=anybody/g' /etc/X11/Xwrapper.config
echo allowed_users=anybody >>/etc/X11/Xwrapper.config
```

4. reboot the system 
