jq -- command to extract fields from json
---

1. extract muliple fields as strings

users.json:
```json
{
    "users": [
        {
            "first": "Stevie",
            "last": "Wonder"
        },
        {
            "first": "Michael",
            "last": "Jackson"
        }
    ]
}
```

```shell
#cat users.json | jq '.users[]|.first'

"Stevie"
"Michael"
```


2. extract muliple fields as new json/dict
```shell
#cat users.json | jq '{.users[]|{"first":.first}}'
{
  "first": "Stevie"
}
{
  "first": "Michael"
}
```
 also we can use regex, find fields which first name contains `M`
 ```shell
 # cat users.json |jq -r  '.users[]|select(.first|test(".*M.*"))'
 {
  "first": "Michael",
  "last": "Jackson"
  }

 #cat users.json |jq -r  '.users[]|select(.first|test(".*M.*"))|.last'
 Jackson
 ```
  another example `project.json`
  ```json
  {
    "projects": [
      {
        "projectId": 4407472,
        "projectName": "acb-dev",
        "projectToken": "585742c994f74949dbbbcd987ea94"
      },
      {
        "projectId": 4422028,
        "projectName": "acb-2108",
        "projectToken": "3d5bc26696d846af82e37d512a2976"
      },
      {
        "projectId": 4422029,
        "projectName": "acb-test",
        "projectToken": "3d5bc26696d846af82e37d512a2946"
      },
      {
        "projectId": 4422030,
        "projectName": "bcd-dev",
        "projectToken": "3d5bc26696d846af82e37d512a2974"
      },
      {
        "projectId": 4422031,
        "projectName": "bcd-test",
        "projectToken": "3d5bc26696d846af82e37d512a2974"
      },
      {
        "projectId": 4422032,
        "projectName": "bcd-2108",
        "projectToken": "3d5bc26696d846af82e37d512c2974"
      }
    ],
    "platform": "aws"
  }
  ```
  ```shell
  # cat project.json|jq  -r '.projects[] |select(.projectName|test(".*acb.*"))|select(.projectName|test(".*^(dev|2108)$"))'
  {
    "projectId": 4407472,
    "projectName": "acb-dev",
    "projectToken": "585742c994f74949dbbbcd987ea94"
  }
  {
    "projectId": 4422028,
    "projectName": "acb-2108",
    "projectToken": "3d5bc26696d846af82e37d512a2976"
  }
  ```

# filter out a image from kubernetes deployment

    ```
    export deploy=message-srv
    export container=message-srv
    kubectl get deploy $deploy  -n integration -o json | jq --arg container $container '.spec.template.spec.containers[]| select(.name|test($container))|.image'
    ```

1. in shell scripts, use `read -n 1 -s -r -p "Press any key to continue"` to implement stop/contine actions

2. to search packages dependencies provides by `pkgconfig(Qt5Widgets) is needed by xxxx`

    ```sh
    The pkg-config files are usually provided by the -devel package so in most cases foo.pc is provided by libfoo-devel. That's still guesswork, but there are two shortcuts:

    Installing by path name, if you know where the .pc file will end up

    $> yum install /usr/lib64/pkgconfig/foo.pc
    That works for any file, but you still need to guess where the .pc file is. The best approach is using the actual pkgconfig requirement:

    $> yum install "pkgconfig(foo)"
    Use the quotes to avoid the shell trying to interpret the parenthesis.
    ```

5 config for download youtube

- ~/.config/youtube-dl/config

  ```config
  --proxy socks5://localhost:38080
  --sub-lang en,zh-CN
  --write-sub
  --embed-subs
  --sub-format srt
  --convert-subs srt
  -f bestvideo+bestaudio/best
  -o '%(playlist_index)s - %(title)s.%(ext)s'
  ```

- ~/.config/yt-dlp/config

  ```config
  -o '%(playlist_index)s - %(title)s.%(ext)s'
  --proxy socks5://localhost:38080
  -f bestvideo+bestaudio/best
  --embed-subs --write-auto-subs  --sub-langs en
  --merge-output-format mp4
  --postprocessor-args "Merger+ffmpeg_i1: -hwaccel cuda"
  --postprocessor-args "Merger+ffmpeg_o1:  -c:v h264_nvenc -c:a libmp3lame"
  ```

  > since postprocess will invoke ffmpeg, I recompiled ffmpeg with nvidia hardware accelerate enabaled.
  >
6. compile ffmpeg with nvidia hardware accelerate support
   - install ffnvcodec

    ```sh
    git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
    cd nv-codec-headers && sudo make install && cd –
    ```

- re-compile ffmpeg

    ```sh
    git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
    sudo yum install -y  libchromaprint-devel.x86_64  frei0r-devel   ladspa-devel dietlibc-devel lilv-devel.x86_64  libbluray-devel.x86_64  libbs2b-devel.x86_64   libdav1d-devel.x86_64  gsm-devel.x86_64  ilbc-devel.x86_64  intel-mediasdk-devel  libmodplug-devel.x86_64  libmysofa-devel.x86_64  libopenmpt-devel.x86_64  libplacebo-devel.x86_64  rav1e-devel.x86_64  rubberband-devel.x86_64   soxr-devel    libssh-devel.x86_64  svt-av1-devel   vo-amrwbenc-devel.x86_64  zeromq-devel.x86_64 zvbi-devel.x86_64  libcdio-paranoia-devel.x86_64 libcdio-devel.x86_64
    export PATH=$PATH:/usr/local/cuda-12.0/bin
    ./configure --prefix=/usr --bindir=/usr/bin --datadir=/usr/share/ffmpeg --docdir=/usr/share/doc/ffmpeg --incdir=/usr/include/ffmpeg --libdir=/usr/lib64 --mandir=/usr/share/man --arch=x86_64 --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3 --enable-bzlib --enable-chromaprint --disable-crystalhd --enable-fontconfig --enable-frei0r --enable-gcrypt --enable-gnutls --enable-ladspa --enable-libaom --enable-libdav1d --enable-libass --enable-libbluray --enable-libbs2b --enable-libcdio --enable-libdrm --enable-libjack --enable-libjxl --enable-libfreetype --enable-libfribidi --enable-libgsm --enable-libilbc --enable-libmp3lame --enable-libmysofa --enable-nvenc --enable-openal --enable-opencl --enable-opengl --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-libplacebo --enable-librsvg --enable-librav1e --enable-librubberband --enable-libsmbclient --enable-version3 --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtesseract --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libv4l2  --enable-libvmaf --enable-version3 --enable-vapoursynth --enable-libvpx --enable-vulkan --enable-libshaderc --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libxml2 --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-avfilter --enable-libmodplug --enable-postproc --enable-pthreads --disable-static --enable-shared --enable-gpl --disable-debug --disable-stripping --shlibdir=/usr/lib64 --enable-lto --enable-libmfx --enable-runtime-cpudetect --enable-nonfree --enable-cuda-nvcc --enable-libnpp --extra-cflags=' -I/usr/include/rav1e -I/usr/local/cuda-12.0/include' --extra-ldflags=-L/usr/local/cuda-12.0/lib64 --nvccflags='-allow-unsupported-compiler'
    make -j
    sudo make install
    ```

- use ffmpeg to covert media files

  ```sh
  ffmpeg -hwaccel cuda   -i input-video.webm -i input-audio.webm  -c:v h264_nvenc -c:a libmp3lame output.mp4
  ```

- use ffmpeg to embed subtitles

  ```sh
  ffmpeg -y -loglevel repeat+info -i file:input.mp4 -i file:input.en.vtt -map 0 -dn -ignore_unknown -c copy -c:s mov_text -map -0:s -map 1:0 -metadata:s:s:0 language=eng -metadata:s:s:0 handler_name=English -metadata:s:s:0 title=English -movflags +faststart file:output.mp4
  ```

7. for loop to deal with files with spaces in names in

- in zsh

    ```zsh
    for file (**/*.txt(ND.)) {ls -l $file}
    ```

    > ((D) to also include hidden files, (N) to avoid the error if there's no match, (.) to restrict to regular files.)
- in bash

  ```bash
  shopt -s globstar nullglob dotglob
  for file in **/*.webm; do
    [ -f "$file" ] || continue
    [ -L "$file" ] && continue
    ls -l "$file"
  done
  ```
8. mpv with hardware acceleration, modify or create `/.config/mpv/mpv.conf`
  ```
  vo=gpu
  hwdec=nvdec
  ```
  or 
  ```
  vo=gpu
  hwdec=nvdec-copy
  ```
  
