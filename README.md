To start testing:
1) git clone https://github.com/tonymorony/trollbox_gui
2)   * sudo apt-get install python3 python3-pip libssl-dev
     * pip3 install requests
     * pip3 install wheel
     * pip3 install kivy 
     * pip3 install python-bitcoinlib
     * pip3 install slick-bitcoinrpc
3) * Hardcode your RPC credentials here for chain on which you want to test (I'm using CCNG now - can share the details if needed): https://github.com/tonymorony/trollbox_gui/blob/master/main.py#L154
* And run as python3 main.py
Then logic as in trollbox scripts (https://github.com/StakedChain/trollbox) - create nickname/oracle/subscribe if needed. 
There will nothing happens in gui on most of the actions which done via pop-up menus but you should see output in console
