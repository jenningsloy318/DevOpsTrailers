## Configure XRDP for mate-desktop 
1. install package 
    ```
    apt install xrdp xorgxrdp -y
    ```
    or 
    ```
    yum install xorgxrdp.x86_64 xrdp.x86_64
    ```
2. create new startmate.sh on mate environment 
    ```
    cat >> /etc/xrdp/startmate.sh << EOF
    #!/bin/sh
    export XDG_CURRENT_DESKTOP=MATE
    exec /etc/xrdp/startwm.sh
    EOF
    chmod a+x /etc/xrdp/startmate.sh
    ```
    or on other desktop environment
    ```
    cat >> /usr/libexec/xrdp/startgnome.sh  << EOF
    #!/bin/sh
    export XDG_CURRENT_DESKTOP=GNOME
    exec /usr/libexec/xrdp/startwm.sh
    EOF

    chmod a+x /usr/libexec/xrdp/startgnome.sh
    ```

    modify startwm-bash.sh
    ```
    sed -i -e '2a export XDG_CURRENT_DESKTOP=MATE' /usr/libexec/xrdp/startwm-bash.sh 
    ```
    or
    ```
    sed -i -e '2a export XDG_CURRENT_DESKTOP=GNOME' /usr/libexec/xrdp/startwm-bash.sh 
    ```
3. modify config 

    ```
    sed -i_orig -e 's/^TerminalServerUsers/#TerminalServerUsers/g' /etc/xrdp/sesman.ini
    sed -i_orig -e 's/^TerminalServerAdmins/#TerminalServerAdmins/g' /etc/xrdp/sesman.ini
    sed -i_orig -e 's/KillDisconnected=false/KillDisconnected=true/g' /etc/xrdp/sesman.ini
    sed -i_orig -e 's/DisconnectedTimeLimit=0/DisconnectedTimeLimit=5/g' /etc/xrdp/sesman.ini
    sed -i_orig -e 's/allowed_users=console/allowed_users=anybody/g' /etc/X11/Xwrapper.config
    echo allowed_users=anybody >>/etc/X11/Xwrapper.config
    sed -i_orig -e 's/crypt_level=high/crypt_level=none/g' /etc/xrdp/xrdp.ini
    sed -i_orig -e 's/security_layer=negotiate/security_layer=rdp/g' /etc/xrdp/xrdp.ini
    ```
    on mate, modify default UserWindowManager 
    ```
    sed -i_orig -e 's/startwm.sh/startmate.sh/g' /etc/xrdp/sesman.ini
    ```
    on gnome, modify default UserWindowManager 
    ```
    sed -i_orig -e 's/startwm.sh/startgnome.sh/g' /etc/xrdp/sesman.ini
    ```
4. config /etc/pam.d/xrdp-sesman
    ```
    #%PAM-1.0
    session required pam_env.so readenv=1 user_readenv=0
    @include common-auth
    @include common-account
    @include common-session
    @include common-password
    ```
5. create ~/.Xclients if on Centos/rhel
    ```
    $ echo "mate-session" > ~/.Xclients
    $ chmod a+x ~/.Xclients
    ```
5. create ~/.xsession
    ```
    echo "mate-session" > ~/.xsession
    ```
6. config ~/.xsessionrc
   ```
    export XDG_SESSION_DESKTOP=mate
    export XDG_DATA_DIRS=${XDG_DATA_DIRS}
    export XDG_CONFIG_DIRS=/etc/xdg/xdg-mate:/etc/xdg
   ```
7. create policies 
   - Create color manager policy,/etc/polkit-1/localauthority/50-local.d/45-allow.colord.pkla
   ```
    [Allow Colord all Users]
    Identity=unix-user:*
    Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
    ResultAny=no
    ResultInactive=no
    ResultActive=yes
   ```
   -  Create package manager policy /etc/polkit-1/localauthority/50-local.d/46-allow-update-repo.pkla
   ```
    [Allow Package Management all Users]
    Identity=unix-user:*
    Action=org.freedesktop.packagekit.system-sources-refresh
    ResultAny=yes
    ResultInactive=yes
    ResultActive=yes
   ```
   - Create Network manager Wifi Scan policy /etc/polkit-1/localauthority/50-local.d/47-allow-wifi-scan.pkla
   ```
    [Allow WiFi Scan all Users]
    Identity=unix-user:*
    Action=org.freedesktop.NetworkManager.wifi.scan
    ResultAny=no
    ResultInactive=no
    ResultActive=yes
   ```


8. reboot the system 
