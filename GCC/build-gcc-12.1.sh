
#!/bin/bash
sudo dnf groupinstall -y "Development tools"

sudo dnf install -y  mpfr-devel gmp-devel libmpc-devel \
zlib-devel glibc-devel.i686 glibc-devel isl-devel \
g++ gcc-gnat gcc-gdc libgphobos-static

mkdir build
cd build
../configure --enable-bootstrap \
--enable-languages=c,c++,fortran,objc,obj-c++,ada,go,d,lto \
--prefix=/opt/gcc/12.1 --program-suffix=-12.1 \
--enable-shared --enable-threads=posix \
--enable-checking=release --enable-multilib --with-system-zlib \
--enable-__cxa_atexit --disable-libunwind-exceptions \
--enable-gnu-unique-object --enable-linker-build-id \
--with-gcc-major-version-only --enable-libstdcxx-backtrace \
--with-libstdcxx-zoneinfo=/usr/share/zoneinfo --with-linker-hash-style=gnu \
--enable-plugin  --with-isl \
--enable-offload-targets=nvptx-none --enable-offload-defaulted \
--enable-gnu-indirect-function --enable-cet --with-tune=generic \
--build=x86_64-redhat-linux \
--with-build-config=bootstrap-lto --enable-link-serialization=1 \
--with-default-libstdcxx-abi=new --with-build-config=bootstrap-lto

make -j 10

sudo make install

