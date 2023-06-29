1. settings for wsl, add options to /etc/wsl.conf
    ```conf
    [boot]
    systemd=true

    [automount]
    enabled = true
    options = "metadata,uid=1000,gid=1000,umask=22,fmask=11,case=off"
    mountFsTab = true

    [network]
    generateHosts = true
    generateResolvConf = true

    [user]
    default=root
    ```

2. reclaim the disk space under wsl2

    2.1 locate the disk file, primaryly in `C:\Users\jenningsl\AppData\Local\Packages\CanonicalGroupLimited.UbuntuPreview_79rhkp1fndgsc\LocalState\ext4.vhdx`

    2.2 create diskpart.txt, with following content
    ```cmd
    select vdisk file="C:\Users\jenningsl\AppData\Local\Packages\CanonicalGroupLimited.UbuntuPreview_79rhkp1fndgsc\LocalState\ext4.vhdx"
    attach vdisk readonly
    compact vdisk
    detach vdisk
    ```
    execute it in administrator powershell  ``` diskpart /s diskpart.txt ```

    2.3 we can still use `optimize-vhd -Path .\ext4.vhdx -Mode full` in administrator powershell