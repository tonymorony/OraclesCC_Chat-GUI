[![Documentation Status](https://readthedocs.org/projects/trollbox-gui/badge/?version=latest)](https://trollbox-gui.readthedocs.io/en/latest/?badge=latest)

# Installation 

Tested on Ubuntu 18.04 (assuming python 3.6+ is installed by default)

```
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get install python3-pip libssl-dev cython3 libgl-dev git python3-kivy
pip3 install requests wheel python-bitcoinlib python-bitcoinrpc pygame
git clone https://github.com/tonymorony/trollbox_gui
cd trollbox_gui
python3 main.py
```

# RPC Connection

* Hardcode your RPC credentials here for chain on which you want to test (I'm using CCNG now - can share the details if needed): https://github.com/tonymorony/trollbox_gui/blob/master/main.py#L154

* If you want to use not local but some remote host for RPC connection you can hardcode it in rpclib here: https://github.com/tonymorony/trollbox_gui/blob/master/rpclib.py#L8


# Usage 

Then logic as in trollbox scripts (https://github.com/StakedChain/trollbox) - create nickname/oracle/subscribe if needed. 
At the moment there nothing happens in gui on most of the actions which done in pop-up menus but you should see output in the same console from which you ran it.
