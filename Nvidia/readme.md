nvidia-docker
---

1. nvidia-cuda docker image
   1. docker pull nvidia/cuda:12.1.0-devel-ubuntu18.04
   2. docker pull nvidia/cuda:12.1.0-devel-ubuntu20.04

2. nvidia-toolkit <https://github.com/NVIDIA/nvidia-docker>
   - installation

   ```bash
   curl -s -L https://nvidia.github.io/libnvidia-container/centos8/libnvidia-container.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
    sudo dnf install nvidia-docker2
    ```

    Edit `/etc/nvidia-container-runtime/config.toml` and disable cgroups:

    ```
    no-cgroups = true
    ```

3. run nvidia docker

   ```
   docker run --privileged --gpus all nvidia/cuda:12.1.0-devel-ubuntu20.04 nvidia-smi
    ```
