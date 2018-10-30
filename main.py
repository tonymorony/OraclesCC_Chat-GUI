from kivy.app import App
from kivy.config import Config
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout


Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

import rpclib
import chatlib


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

    def get_rooms_list(self):
        self.data = chatlib.get_chat_rooms(TrollboxCCApp.rpc_connection)
        return self.data

    def on_text(instance, value):
        print('The widget', instance, 'have:', value)

    def send_message(instance, showid, inputid):
        showid.item_strings.append(inputid.text)
        inputid.text = ''

    def callback_refresh_rooms(self, roomslist):
        roomslist.adapter.data = self.get_rooms_list()


class MainBox(BoxLayout):
    pass


class ChatsArea(BoxLayout):

    def get_data(self):
        self.lv1.data = rpclib.oracles_list(TrollboxCCApp.rpc_connection)


if __name__ == "__main__":
    TrollboxCCApp().run()
