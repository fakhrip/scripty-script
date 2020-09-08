wget -O discord.deb https://discord.com/api/download?platform=linux&format=deb
wget -O steam.deb https://cdn.cloudflare.steamstatic.com/client/installer/steam.deb
wget -O ghidra.zip https://ghidra-sre.org/ghidra_9.1.2_PUBLIC_20200212.zip
wget -O cutter https://github.com/radareorg/cutter/releases/download/v1.12.0/Cutter-v1.12.0-x64.Linux.appimage

sudo dpkg -i discord.deb
sudo dpkg -i steam.deb

unzip ghidra.zip

sudo cp cutter /usr/bin
sudo cp cutter /bin
rm cutter

sudo snap install --classic code
sudo snap install spotify

sudo apt-get install exiftool python python3 python3-pip python-pip spotify-client radare2 firefox chromium-browser wireshark audacity 