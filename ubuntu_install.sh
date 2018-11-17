#!/bin/bash
set -euo pipefail

echo "Setting up kivy and needed packages"

sudo apt-get update
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get install python3-pip libssl-dev cython3 libgl-dev git python3-kivy

echo "Setting up needed pip packages"

pip3 install requests wheel python-bitcoinlib python-bitcoinrpc pygame

echo "Installing trollbox"

cd ~
git clone https://github.com/tonymorony/trollbox_gui

touch ~/trollbox_gui/run.sh
current_user="$(whoami)"
chmod u+x ~/trollbox_gui/run.sh
chown $current_user:$current_user ~/trollbox_gui/run.sh

echo "#!/bin/bash" >> ~/trollbox_gui/run.sh
echo "python3 $HOME/trollbox_gui/main.py" >> ~/trollbox_gui/run.sh

touch ~/Desktop/TrollboxGUI.desktop
chmod a+x ~/Desktop/TrollboxGUI.desktop

echo "[Desktop Entry]" >> ~/Desktop/TrollboxGUI.desktop
echo "Type=Application" >> ~/Desktop/TrollboxGUI.desktop
echo "Exec=$HOME/trollbox_gui/run.sh" >> ~/Desktop/TrollboxGUI.desktop
echo "Name=TrollboxGUI" >> ~/Desktop/TrollboxGUI.desktop
echo "Terminal=true" >> ~/Desktop/TrollboxGUI.desktop
echo "Icon=$HOME/trollbox_gui/favicon.ico" >> ~/Desktop/TrollboxGUI.desktop

echo "Installation completed"