Desktop Environment tuning
---

## Backgroud
Starting from Aug 2021, I transmit desktop enviromnent from mate desktop to lxqt as mate didn't have a regular new release which indicates its inactive development while lxqt is in better shape



## LXQT
- As current lxqt-session heavily depends on openbox, I re-comiled  release 0.17.0 and removed the openbox dependencies
- after removed openbox, I have multiple window manager choices, i choose kwin as it support Nvidia prepietory driver which in return support wayland on Nvidia 
- follow lxqt build guide [Building-from-source](https://github.com/lxqt/lxqt/wiki/Building-from-source)
- grab SRPM from [dyn repo](https://pkgs.dyn.su/el8/base/SRPMS/)
- other software choices
  - screenshot: flameshot
  - calculator: speedCrunch
  - display manager: sddm
  - window manager: kwin
  - editor: FeatherPad
  - terminal: Qterminal
- configurations
  - configure sddm
    ```conf
    [General]
    InputMethod=  ## set it to none will disable virtual keyboard pop up at login window
    Numlock=on
    
    [Theme]
    Current=02-lxqt-fedora

    [Wayland]
    EnableHiDPI=true ## enable HiDPI for Wayland

    [X11]
    EnableHiDPI=true ## enable HiDPI for X11
    ```
  - change lxqt default session, use `Preferences ---> Session Settings`, or modify ~/.config/lxqt/session.conf
    - set default `window_manager` to `kwin_x11`
    - enable hiDPI for windows, add environments
      ```conf
      [Environment]
      GDK_SCALE=2  ## set scale for gtk to 2 
      GTK_CSD=1    ## enable client side decoration
      GTK_OVERLAY_SCROLLING=1 ## overlay scrollbars are enabled by default, meaning that scrollbars will be shown only on mouseover in GTK 3 applications
      GTK_USE_PORTAL=1 ## order to have the same file dialog on qt5 for gtk applications, one can use XDG Portals
      QT_AUTO_SCREEN_SCALE_FACTOR=1 ## Qt 5 applications can be instructed to honor screen DPI by setting the QT_AUTO_SCREEN_SCALE_FACTOR
      QT_SCALE_FACTOR=1 ## If automatic detection of DPI does not produce the desired effect, scaling can be set manually per-screen (QT_SCREEN_SCALE_FACTORS) or globally (QT_SCALE_FACTOR)
      ```

      links: 
      - https://wiki.archlinux.org/title/HiDPI
      - https://wiki.archlinux.org/title/Uniform_look_for_Qt_and_GTK_applications

      notes:
      - before `GTK_USE_PORTAL` is configured, gtk application menu button are not displayed 
    - configure themes
      - widget style: breeze
      - icon theme: breeze
      - LXQT theme: kde-plasma
      - Cursor: breeze
  - configure audio output
    - as I have a jraba user microphone, so i'd like to set it as default, don't have other output
      ```shell
      ~ pactl list short sinks
      42      alsa_output.pci-0000_29_00.3.iec958-stereo      PipeWire        s32le 2ch 48000Hz       RUNNING
      41      alsa_output.pci-0000_27_00.1.hdmi-stereo-extra2 PipeWire        s32le 2ch 48000Hz       SUSPENDED
      59      alsa_output.usb-0b0e_Jabra_BIZ_2400_USB_1C48F9368626x014200-00.pro-output-0     PipeWire        s16le 2ch 48000Hz       SUSPENDED
      ```
    - config `/etc/pulse/client.conf`, modify `default-sink`
      ```conf 
      default-sink = alsa_output.usb-0b0e_Jabra_BIZ_2400_USB_1C48F9368626x014200-00.pro-output-0
      ```
    - start play something and check it again
      ```
      ~  pactl list short sinks 
      42      alsa_output.pci-0000_29_00.3.iec958-stereo      PipeWire        s32le 2ch 48000Hz       SUSPENDED
      41      alsa_output.pci-0000_27_00.1.hdmi-stereo-extra2 PipeWire        s32le 2ch 48000Hz       SUSPENDED
      59      alsa_output.usb-0b0e_Jabra_BIZ_2400_USB_1C48F9368626x014200-00.pro-output-0     PipeWire        s16le 2ch 48000Hz       RUNNING
      ~ pactl info
      Server String: /run/user/1000/pulse/native
      Library Protocol Version: 34
      Server Protocol Version: 35
      Is Local: yes
      Client Index: 146
      Tile Size: 65472
      User Name: jenningsl
      Host Name: workstation
      Server Name: PulseAudio (on PipeWire 0.3.33)
      Server Version: 15.0.0
      Default Sample Specification: float32le 2ch 48000Hz
      Default Channel Map: front-left,front-right
      Default Sink: alsa_output.usb-0b0e_Jabra_BIZ_2400_USB_1C48F9368626x014200-00.pro-output-0
      Default Source: alsa_input.usb-0b0e_Jabra_BIZ_2400_USB_1C48F9368626x014200-00.pro-input-0
      Cookie: 3eb7:5432
      ```