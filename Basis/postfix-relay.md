## configure postfix as relay server
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
mynetworks = 10.36.50.0/24 10.36.51.0/24 10.36.52.0/24
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

## restrictions about which hosts can leverage this host as relay host to send out email
smtpd_relay_restrictions = permit_mynetworks,  permit_sasl_authenticated, reject_unauth_destination
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

then
```
postmap /etc/postfix/relay_credential
postmap /etc/postfix/generic
```

finally
```
systemctl start postfix
```