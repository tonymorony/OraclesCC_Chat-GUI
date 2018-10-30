from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.popup import Popup
from kivy.uix.listview import ListView


import rpclib
import chatlib


class MyListView(BoxLayout):
    pass

class TrollboxCCApp(App):

    title = "OraclesCC Trollbox"
    pass


if __name__ == "__main__":
    while True:
        try:
            rpc_connection = rpclib.rpc_connect("user3941991022", "pass89db79d7ef9ea31392cb9fdc52163ee8c5e95b5c0e3bbc687cb638720413b8b4d4", 56212)
            rpclib.getinfo(rpc_connection)
        except Exception:
            print("Cant connect to RPC! Please re-check credentials.", "pink")
        else:
            print("Succesfully connected!")
            break
    TrollboxCCApp().run()
