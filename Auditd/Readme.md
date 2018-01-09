**auditd** is a audit service running on most linux, based on pre-configured rules, Audit generates log entries to record as much information about the events that are happening on your system as possible

---
audit.rules: is a file containing audit rules that will be loaded by the audit daemon's init script whenever the daemon is started. The audit rules come in 3 varieties: control, file, and syscall.

- Control

    Control commands generally involve configuring the audit system rather than telling it what to watch for. These commands typically include deleting all rules, setting the size of the kernel's backlog queue, setting the failure mode, setting the event rate limit, or to tell auditctl to ignore syntax errors in the rules and continue loading. Generally, these rules are at the top of the rules file.

- File System

    File System rules are sometimes called watches, The syntax of these rules generally follow this format: 
    ```rukes
    -w path-to-file -p permissions -k keyname
    ```
    * path_to_file:  is the file or directory that is audited.
    * permissions are the permissions that are logged:
        - r: read of the file
        - w： write to the file
        - x: execute the file
        - a:  change in the file's attribute
    * key_name: is an optional string that helps you identify which rule or a set of rules generated a particular log entry.

- System Call
    
    The Linux kernel has 4 rule matching lists or filters as they are sometimes called. They are: **task, exit, user, and exclude**

    - The **task** list:  is checked only during the fork or clone syscalls. It is rarely used in practice.
    - The **exit** filter: is the place where all syscall and file system audit requests are evaluated.
    - The **user** filter: is used to filter (remove) some events that originate in user space. By default, any event originating in user space is allowed. So, if there are some events that you do not want to see, then this is a place where some can be removed
    - The **exclude** filter： is used to exclude certain events from being emitted


    Syscall rules take the general form of:
    ```rules
    -a action,list -S syscall -F field=value -k keyname
    ```

    - The **-a** option tells the kernel's rule matching engine that we want to append a rule at the end of the rule list(task,exit,user,exclude).
        * always:  always create an event
        * never: never create an event
    - Replacing -a with -A in the above command will insert the rule at the top instead of at the bottom.
    - The **-S** option. This field can either be the syscall name or number,For readability, the name is almost always used, You may give more than one syscall in a rule by specifying another -S option
    - The **-F** options that fine tune what to match against. field=value specifies additional options that furthermore modify the rule to match events based on a specified architecture, group ID, process ID, and others. For a full listing of all available field types and their values, see the auditctl(8) man page. ` -F [n=v | n!=v | n<v | n>v | n<=v | n>=v | n&v | n&=v]`
            
            
    - The **key_name** is an optional string that helps you identify which rule or a set of rules generated a particular log entry.

---

Scenario:
1. audit all command list

    ```
    -a exit,always -F arch=b64,audit.kernel.action=executed  -S execve 
    -a exit,always -F arch=b32,audit.kernel.action=executed  -S execve
    ```

2. use auditbeat to achieve the same function
    
    2.1 install auditbeat
    ```shell
    curl -L -O https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-6.0.1-amd64.deb
    dpkg -i auditbeat-6.0.1-amd64.deb
    ```
    2.2 configure auditbeat in /etc/auditbeat/auditbeat.yml,example is [auditbeat.yml](./auditbeat.yml)
    
    2.3 be aware to stop auditd when use auditbeat to gather the audit info



