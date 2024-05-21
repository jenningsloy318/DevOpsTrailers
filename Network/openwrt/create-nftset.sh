
#!/bin/bash
declare -a ipArray

for domain in $(cat gfwlist.txt)

    do
        IPs=$(dig +short ${domain}|grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
        if [ "x${IPs}" != "x" ]; then
        for ip in ${IPs}
        do
            ipArray+=(${ip})
        done
        fi
    done
items=$(IFS=,; printf '%s' "${ipArray[*]}")


cat <<EOF > gfwlist.nft

set gfwlist {
	type ipv4_addr
	flags interval
	elements = { ${items} }
}

chain gfwlist-redirect {
	type nat hook prerouting priority 0; policy accept;
	ip daddr @gfwlist ip protocol tcp redirect to :38080
}
EOF