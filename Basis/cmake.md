cmake
---
1. build and install 
    ```
    cmake -B build-dir -S source-dir
    cmake --build build-dir  
    cmake --install build-dir 
    ```
2. uninstall if `install_manifest.txt` is created in `build-dir`
   ```
   xargs rm < install_manifest.txt
    ```