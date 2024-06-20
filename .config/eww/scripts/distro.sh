#!/bin/bash

# Define the icons for each distribution.
iconos=(
  ['ubuntu']=''
  ['debian']=''
  ['fedora']=''
  ['nix']='󱄅'
  ['manjaro']=''
  ['mx_linux']=''
  ['mint']='󰣭'
  ['deepin']=''
  ['zorin_os']=''
  ['centOs']=''
  ['redhat']=''
  ['opensuse']=''
  ['arch']='󰣇'
  ['archcraft']=''
  ['endeavouros']=''
)

# Get the distribution name
OS=$(awk -F= '/^ID=/{gsub(/"/, "", $2); print $2}' /etc/os-release)

# Configure content based on distribution
content=${iconos[$OS]}

# If no icon was found for the distribution, use a default icon
if [ -z "$content" ]; then
  content="icono_predeterminado"
fi

echo $content
