# Add Linux host to Azure Active Directory


- Install requred packages

```sh
dnf install -y realmd sssd adcli krb5-workstation krb5-libs oddjob oddjob-mkhomedir samba-common-tools
```

- Dicover the domain

```sh
realm discover EXAMPLE.DOMAIN.COM
```

- Initialize Kerberos using the kinit command

```sh
kinit admin@EXAMPLE.DOMAIN.COM
```

- Join the domain

```sh
realm join --verbose --client-software=sssd EXAMPLE.DOMAIN.COM -U 'admin@EXAMPLE.DOMAIN.COM'
```



refer to [Join a Red Hat Enterprise Linux virtual machine to an Azure Active Directory Domain Services managed domain](https://docs.microsoft.com/en-us/azure/active-directory-domain-services/join-rhel-linux-vm)
