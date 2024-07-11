# Create rootfs

## Create rootfs for yum based docker container

- on host, install anaconda and livemedia

  ```sh
  dnf install -y anaconda lorax
  ```

- create docker rootfs tar file

  ```sh
  livemedia-creator --make-tar --no-virt --ks=fedora-container.ks   --image-name=fedora-base.tar
  ```

  the file will be created as  /var/tmp/fedora-base.tar

- use a [Dockerfile](./Dockerfile) to create a further docker image

  ```sh
  docker build -t fedora:34 -f Dockerfile .
  ```

## Create rootfs for debian/ubuntu based docker container

- create ubuntu image

  ```shell
  debootstrap --arch=amd64 --variant=minbase --make-tarball=focal.tar  focal focal-root/
  ```
