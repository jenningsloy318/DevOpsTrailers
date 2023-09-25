
1. define service in firewalld
```
firewall-cmd --permanent --new-service=jenkins
firewall-cmd --permanent --service=jenkins --set-short="Jenkins Service Ports"
firewall-cmd --permanent --service=jenkins --set-description="Jenkins service firewalld port exceptions"
firewall-cmd --permanent --service=jenkins --add-port=8080/tcp
firewall-cmd --permanent --add-service=jenkins
```

2. add service in zone
```
firewall-cmd --zone=public --add-service=http --permanent
```

3. add a port directly

```
firewall-cmd --zone=public --add-port=9093/tcp --permanent
```


4. reload the firewll to take effect

```
firewall-cmd --reload
```



5. configure Centos as a router
```
firewall-cmd --permanent --direct --passthrough ipv4 -t nat -I POSTROUTING -o ens224u2 -j MASQUERADE -s 192.168.2.0/24
firewall-cmd --permanent --direct --passthrough ipv4 -t nat -I POSTROUTING -o ens224u2 -j MASQUERADE -s 192.168.1.0/24
firewall-cmd --permanent --direct --passthrough ipv4 -t nat -I POSTROUTING -o ens224u2 -j MASQUERADE -s 10.36.0.0/16

firewall-cmd --change-interface=ens224u2 --zone=external --permanent

firewall-cmd --set-default-zone=internal

firewall-cmd --complete-reload
```


6. add forward port

```
firewall-cmd  --add-masquerade --permanent
firewall-cmd --permanent --add-forward-port=port=41443:proto=tcp:toaddr=10.36.51.141:toport=443
firewall-cmd --permanent --add-forward-port=port=42443:proto=tcp:toaddr=10.36.51.142:toport=443
firewall-cmd --permanent --add-forward-port=port=11443:proto=tcp:toaddr=10.36.51.11:toport=443
firewall-cmd --add-port={41443/tcp,42443/tcp,11443/tcp} --permanent
```

7. block certain app to access internet

    nftables can set firewall rules based on cgroups (it can be bound to each program), the syntax:
    ```
    socket cgroupv2 level NUM PATH
    ```

    - 'PATH': is the one in /sys/fs/cgroup, note that the 'PATH' is relative, so you should exclude /sys/fs/cgroup/ from the absolute path. For example, /sys/fs/cgroup/system.slice/nginx.service is the cgroup for nginx and its 'PATH' should be system.slice/nginx.service.

        Most systemd services are confined in cgroups. Use systemd-cgls to view the cgroup tree and use systemd-cgls -u XXX.service to get the cgroup for a specific service. For example, `systemd-cgls -u nginx.service` returns `/system.slice/nginx.service`.

        Note that you should remove the first / , so the 'PATH' should be `system.slice/nginx.service`. If your path contains the symbol '@' please use nft --interactive to set up your firewall rules, other wise, the symbol would be misinterpreted.

        Although cgroups will be setup for every systemd unit automatically, you can modify or create systemd unit files to fine tune the cgroup settings if you have special needs. Theoretically, you can set up rules for all programs in a systemd enabled operating system. See `systemd.unit(5)` and `systemd.slice(5)` for more information.



    - 'NUM': indicates the level of cgroups that will be matched in the firewall rule. In our previous example, `socket cgroupv2 level 2 "system.slice/nginx.service"` matches exactly the nginx service. While `socket cgroupv2 level 1 "system.slice/nginx.service"` matches all the cgroups under `"system.slice/"`, thus not only nginx but other programs in that directory will also be matched, such as "snapd.service".



    To prevent nginx from accessing the Internet (assume you already have a inet table named 'filter' and a chain named 'output'):

    ```
    nft add rule inet filter output socket cgroupv2 level 2 "system.slice/nginx.service" drop
    ```

8. rich rules

```
firewall-cmd --permanent  --add-rich-rule='rule family="ipv4" source address="10.0.0.0/24" port protocol="tcp" port="38080" accept'
```
