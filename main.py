from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

import rpclib

class TrollboxCCApp(App):

    title = "OraclesCC Trollbox"

    while True:
        try:
            rpc_connection = rpclib.rpc_connect("user3941991022", "pass89db79d7ef9ea31392cb9fdc52163ee8c5e95b5c0e3bbc687cb638720413b8b4d4", 56212)
            rpclib.getinfo(rpc_connection)
        except Exception:
            print("Cant connect to RPC! Please re-check credentials.", "pink")
        else:
            print("Succesfully connected!")
            break


if __name__ == "__main__":
    TrollboxCCApp().run()
