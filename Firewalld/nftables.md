nftables
---

1. basic operations

* list tables

```shell
root@websvc:~#  nft list tables
table inet filter
```

* show chains in the table

```shell
root@websvc:~#  nft list table inet filter
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}

	chain forward {
		type filter hook forward priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
```

* change default policy of filter input to drop

```shell
root@websvc:~#  nft list table inet filter
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
	}

	chain forward {
		type filter hook forward priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
```

* add rule to chain

```shell
root@websvc:~# nft add inet filter input tcp dport 2017 accept
```

* list the ruleset

```shell
root@websvc:~# nft list table inet filter
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		tcp dport 2017 accept
	}

	chain forward {
		type filter hook forward priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
```

* delete rule, You have to obtain the handle to delete a rule via the `-a` option

```shell
root@websvc:~# nft -a list table nat
table nat { # handle 34
	chain prerouting { # handle 1
		type nat hook prerouting priority dstnat; policy accept;
	}

	chain postrouting { # handle 2
		type nat hook postrouting priority srcnat; policy accept;
		ip saddr 182.148.71.3 snat ip to 92.118.228.104 # handle 5
	}
}
root@websvc:~# nft delete rule nat postrouting handle 5
```

* clear rules

```shell
root@websvc:~# nft flush ruleset
```

2. allow Allow Established/Related

```shell
root@websvc:~# nft add rule inet filter input ct state established,related accept
```

3. allow port from source

```shell
root@websvc:~# nft add rule inet filter input ip saddr 182.148.71.3 udp dport 6443 accept
root@websvc:~# nft add rule inet filter input ip saddr 182.148.71.3 tcp dport 6443 accept
```

4. add counter and limit

```shell
root@websvc:~# nft add counter inet filter ssh-counter {comment "counter ssh connection"}
root@websvc:~# nft add rule inet filter input tcp dport 2017 meter ssh-conn-meter { ip saddr & 255.255.255.0 ct count 5 } counter name ssh-counter accept
root@websvc:~# nft list counter inet filter ssh-counter
table inet filter {
	counter ssh-counter {
		comment "counter ssh connection"
		packets 1 bytes 64
	}
}
root@websvc:~# nft list meter inet filter ssh-conn-meter
table inet filter {
	meter ssh-conn-meter {
		type ipv4_addr
		size 65535
		flags dynamic
		elements = { 182.149.137.0 ct count 5 }
	}
}
```

4. configure NAT

* create table and chain

```shell
root@websvc:~# nft add table nat
root@websvc:~# nft add chain nat prerouting '{ type nat hook prerouting priority -100 ; policy drop;}'
root@websvc:~# nft add chain nat postrouting '{ type nat hook postrouting priority 100 ; policy drop;}'
```

* configure SNAT

```shell
root@websvc:~# nft add rule nat postrouting ip saddr 10.0.0.0/24 snat to 92.118.228.104
root@websvc:~# nft add rule nat postrouting tcp dport 6443 snat to 92.118.228.104
root@websvc:~# nft add rule nat postrouting udp dport 6443 snat to 92.118.228.104

```
