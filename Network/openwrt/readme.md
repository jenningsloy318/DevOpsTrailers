#  OpenWRT


## enable dockerd use nftables instead of iptables
- add docker bridge to the covered_devices in firewall: Network ---> Firewall ---> Zones ----> docker ---> Edit ---> Advanced Settings ---> Covered devices -----> choose docker0  ----> SAVE; then SAVE & APPLY
- enable docker to forward to wan, Network ---> Firewall ---> Zones ----> docker ---> Edit ---> Allow forward to destination zones: ---> add wan

- Set `option iptables '0'` in /etc/config/dockerd
-  flush iptables
  ```
  iptables -F
  iptables -t nat -F
  ```
- if using docker compose, set `network_mode: bridge` in docker-compose.yml, which uses the docker default bridge
  ```
  services:
    podfetch:
      container_name: podfetch
      image: samuel19982/podfetch:latest
      restart: always
      network_mode: bridge
      #network_mode: host
      ports:
        - "8000:8000"
      volumes:
        - /mnt/sda1/podfetch/podcasts:/app/podcasts
        - /mnt/sda1/podfetch/db:/app/db
      environment:
      ....
  ```
