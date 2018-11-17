[![Documentation Status](https://readthedocs.org/projects/trollbox-gui/badge/?version=latest)](https://trollbox-gui.readthedocs.io/en/latest/?badge=latest)

![alt text](https://i.imgur.com/uamsC8q.png)

# Installation 

Tested on Ubuntu 18.04 (assuming python 3.6+ is installed by default)
And Komodo builded from FSM branch of https://github.com/jl777/komodo/

```
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get install python3-pip libssl-dev cython3 libgl-dev git python3-kivy
pip3 install requests wheel python-bitcoinlib slick-bitcoinrpc pygame
git clone https://github.com/tonymorony/trollbox_gui
cd trollbox_gui
python3 main.py
```

# RPC Connection

* In case of localhost daemon usage use 127.0.0.1 as RPC address. Username, password and port can be found in .conf file for desired asset chain

* If you want to use remote host for RPC connection you need to add your IP as rpcallowip= param to desired asset chain daemon config


# Usage 

Then logic as in trollbox scripts (https://github.com/StakedChain/trollbox) - create nickname/oracle/subscribe if needed. 
At the moment there nothing happens in gui on most of the actions which done in pop-up menus but you should see output in the same console from which you ran it.
