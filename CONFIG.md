> :warning: **If something fails or doesn't work check the dependencies.**: 

<p align="center">
  <picture>
    <img src="/assets/koi.gif">
  </picture>
</p>

- 🌸 [Directory](https://github.com/Shentxt/Hyprhype/tree/master#Dir)
- 🌸 [Install](https://github.com/Shentxt/Hyprhype/tree/master#Install)
- 🌸 [Apps and Font](https://github.com/Shentxt/Hyprhype/tree/master#Pack)

# 📦Dir

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>

Hyprhype
├── .config
│   ├── ags
│   ├── hypr
│   ├── kitty
│   ├── starship
│   ├── cava
│   └── nvim
├── .local
│   ├── bin
│   └── share
├── boot
│   └── grub
├── etc
│   └── greetd
├── .zshrc
├── firefox
│   ├── chrome
│   ├── extensions
│   └── user.js
└── usr
    ├── fonts
    ├── icons
    ├── nsa-plymounth
    └── slice

</code></pre>
</div>

# 💾Install

## Download 

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>
 git clone https://github.com/Shentxt/Hyprhype
 cd Hyprhype
 cp -r .config ~/.config 
 cp -r .local ~/.local
 cp -r chrome extensions user.js /u directory of firefox 
</code></pre>
</div>

## Dowload Dependencies 

> :warning: **If you don't want to download all the dependencies, read dependencies.txt**:

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>
 yay -S --needed - < dependencies.txt
 or 
 paru -S --needed - < dependencies.txt
</code></pre>
</div>

## Removed 

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>
 sudo rm -r Hyprhype
</code></pre>
</div>

# 📦Pack

## Font user 

- monocraft
- minecraft

## Apps 

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>
 amdctl or asusctl (This works for the modes)
</code></pre>
</div>

## Script

<div style="background-color: black; color: white; padding: 10px;">
<pre><code>
  npm install node-notifier sharp chokidar @types/chokidar --save-dev
</code></pre>
</div>

## greetd (necessary if using greeter) 

> :warning: **Read https://aylur.github.io/ags-docs/services/greetd/ and https://sr.ht/~kennylevinsen/greetd/**:

It works, although I had a problem with pam, maybe you guys will have better luck.
The files are in usr. If anyone has been able to run it without problems, let me know and tell me what steps you followed and the distro, I would really appreciate it.

Try this, it worked for me

useradd -M -G video greeter
chmod -R go+r /etc/greetd/

## Plugins 

> :warning: **Read https://hyprland.org/plugins/**: 

- hyprpm add https://github.com/hyprwm/hyprland-plugins
- hyprpm add https://github.com/outfoxxed/hy3
- hyprpm add borders-plus-plus
- hyprpm add hyprbars

- nvim https://docs.astronvim.com/

> :warning: **if you use firefox theme Gx (https://github.com/Godiesc/firefox-gx) need to configure this in about:support and about:config**: 

- firefoxgx.tree-tabs (use it with Tree Style Tab) 
- firefoxgx.tab-shapes
- firefoxgx.main-image
- firefoxgx.left-sidebar

- ui.systemUsesDarkTheme = 1
- ui.useDefaultToolbarTheme = 0
- MOZ_ENABLE_WAYLAND=1 
- browser.tabs.remote.force-enable = true
- extensions.webRequest.allowRequest
