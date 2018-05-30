# configure postfix as relay server

##Basic Configuration
需要关注的配置：
- inet_interfaces
- myhostname：主机名
- mydomain：域名
- myorigin：设置由本级寄出去的邮件所使用的域名或主机名
- mynetworks：设置可转发哪些网络的邮件
- mydestination：设置可接受邮件的主机名和域名
- smtpd_relay_restrictions： 限制哪些主机可以将本机作为relay host做转发

conf:
```
##Basic conf
queue_directory = /var/spool/postfix
command_directory = /usr/sbin
daemon_directory = /usr/libexec/postfix
data_directory = /var/lib/postfix
mail_owner = postfix
inet_interfaces = all
inet_protocols = all
myhostname = yh-vm-smtp-prod01.snfc.org
mydomain = snfc.org
myorigin = $mydomain
inet_interfaces = all
mynetworks = 10.36.50.0/24 10.36.51.0/24 10.36.52.0/24 10.36.48.0/24
mydestination = $myhostname localhost.$mydomain localhost $mydomain $mynetworks
unknown_local_recipient_reject_code = 550
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
debug_peer_level = 2
sendmail_path = /usr/sbin/sendmail.postfix
newaliases_path = /usr/bin/newaliases.postfix
mailq_path = /usr/bin/mailq.postfix
setgid_group = postdrop
html_directory = no
manpage_directory = /usr/share/man
sample_directory = /usr/share/doc/postfix-2.10.1/samples
readme_directory = /usr/share/doc/postfix-2.10.1/README_FILES


## upstream smtp server auth info
relayhost = relayhost:port
smtp_sasl_type = cyrus
smtp_sasl_auth_enable = yes
### smtp_sasl_password_maps: include the authentication user/pass to upstream smtp
smtp_sasl_password_maps = hash:/etc/postfix/relay_credential  
smtp_sasl_security_options = noanonymous
smtp_use_tls = yes
smtp_cname_overrides_servername = no
smtp_sasl_mechanism_filter = plain, login
##smtp_generic_maps: maps the some fromaddr to a particular one
smtp_generic_maps = hash:/etc/postfix/generic


##SMTPD conf

## restrictions about which hosts can leverage this host as relay host to send out email
smtpd_recipient_restrictions = permit_sasl_authenticated,  permit_mynetworks,  defer_unauth_destination
smtpd_relay_restrictions  = permit_sasl_authenticated,  permit_mynetworks,  defer_unauth_destination

```


生成  
/etc/postfix/relay_credential
```
[upstream-smtp-host]:port  login-user:login-pass
```
/etc/postfix/generic:
```
@*.snfc.org  <from-addr>
root@linux.local <from-addr>
root@10.36.51.11 <from-addr>
```

转换postmap
```
postmap /etc/postfix/relay_credential
postmap /etc/postfix/generic
```

最后重启postfix服务
```
systemctl start postfix
```

## Advanced setting for authentication
如果要在本机启用用户认证，添加以下行到`/etc/postfix/main.cf`

```
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $mydomain
broken_sasl_auth_clients = yes
```

然后修改 ` /etc/postfix/sasl/smtpd.conf`
```
pwcheck_method: auxprop
auxprop_plugin: sasldb
mech_list: plain login cram-md5 ntlm
```
创建用户，会保存到`/etc/sasldb2`
```
saslpasswd2 -c -u `postconf -h mydomain` jumpmailuser
```

复制 `/etc/sasldb2` 到`/var/spool/postfix/etc/sasldb2`并修改权限
```
cp /etc/sasldb2 /var/spool/postfix/etc/sasldb2
chmod 644  /var/spool/postfix/etc/sasldb2
```
重启postfix并测试

```
systemctl restart postfix 
```

测试：
```
echo -n jumpmailuser|base64
echo -n pass | base64
---------------------------
telnet localhost 25

Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 yh-bm-ob-mon-prod01 ESMTP Postfix (Ubuntu)
anVtcG1haWx1c2Vy
502 5.5.2 Error: command not recognized
anVtcG1haWx1c2Vy
502 5.5.2 Error: command not recognized
auth login
334 VXNlcm5hbWU6
anVtcG1haWx1c2Vy
334 UGFzc3dvcmQ6
anVtcG1haWx1c2Vy
235 2.7.0 Authentication successful
```