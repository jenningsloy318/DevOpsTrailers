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


3. enable complete right-click menu on win11, execute following command with administrator powershell
    ```
    reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
    ```