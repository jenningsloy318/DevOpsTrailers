# cmake

- build and install

    ```sh
    cmake --fresh  -B build-dir -S source-dir -DCMAKE_INSTALL_PREFIX=/usr
    cmake --build build-dir
    cmake --install build-dir
    ```

    > `--install-prefix /usr`: same with `-DCMAKE_INSTALL_PREFIX=/usr`
- uninstall if `install_manifest.txt` is created in `build-dir`

   ```sh
   xargs rm < install_manifest.txt
    ```