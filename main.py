from kivy.app import App
from kivy.config import Config
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.listview import ListView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from functools import partial


Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')
Config.set('kivy', 'window_icon', 'favicon.ico')

import rpclib
import chatlib
import bitcoinrpc



class MessagesBoxLabel(Label):

    def update(self):
        self.text = TrollboxCCApp.active_room_id


class RoomListItemButton(ListItemButton):

    def on_release(self):
        # setting active room id after room button release
        TrollboxCCApp.active_room_id = str(self.text[-64:])


#have to receive time delta for compatibility with kivy clock
class MessageUpdater(Widget):

    def messages_checker(self, dt):
        while True:
            oracles_info = rpclib.oracles_info(App.get_running_app().rpc_connection, App.get_running_app().active_room_id)
            if App.get_running_app().active_room_id == '':
                print("Seems its work")
                break
            else:
                baton_returned = ''
                #TODO: it should work with only one publisher now
                for entry in oracles_info["registered"]:
                    baton_returned = entry["batontxid"]
            # getting new message to message list only if there any new and changing baton in app for the next check
            if baton_returned != App.get_running_app().current_baton:
                App.get_running_app().current_baton = baton_returned
            else:
                break
            try:
                new_message = rpclib.oracles_samples(App.get_running_app().rpc_connection, App.get_running_app().active_room_id, baton_returned, "1")
                App.get_running_app().messages.append(str(new_message['samples']))
                App.get_running_app().root.ids.messagesview.adapter.data = App.get_running_app().messages
                break
            except bitcoinrpc.authproxy.JSONRPCException as e:
                print(App.get_running_app().active_room_id)
                print(e)
                break


class TrollboxCCApp(App):


    def build(self):
        messenger_gui = Builder.load_file("trollboxcc.kv")
        return messenger_gui

    title = "OraclesCC Trollbox"

    active_room_id = ''

    messages = ["test"]

    current_baton = ''

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

    def on_press(self):
        print("I'm Working!")
        print(self.active_room_id)

    # checking selected chat room for new messages every 0.5 seconds
    message_updater = MessageUpdater()
    check_messages = Clock.schedule_interval(partial(MessageUpdater.messages_checker, message_updater), 0.5)
    check_messages()


if __name__ == "__main__":
    TrollboxCCApp().run()


