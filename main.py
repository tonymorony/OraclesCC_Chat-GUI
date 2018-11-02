from kivy.app import App
from kivy.config import Config
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
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
                print("Seems messages grabbing works")
                break
            else:
                baton_returned = ''
                #TODO: it should work with only one publisher now have to add all publishers support to go public testing
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


class CreateRoomButton(Button):

    def create_room(self, room_name, room_description):

        secret_room_description = "CHAT " + room_description
        try:
            new_room_hex = rpclib.oracles_create(App.get_running_app().rpc_connection, room_name, secret_room_description, "S")
            print(new_room_hex)
        except Exception as e:
            print(e)
        else:
            try:
                new_room_txid = rpclib.sendrawtransaction(App.get_running_app().rpc_connection, new_room_hex["hex"])
                print(new_room_txid)
            except KeyError as e:
                print(e)
                print(new_room_hex)


class CreateNicknameButton(Button):

    def create_nickname(self, nickname, password):
        new_nickname = chatlib.set_nickname(App.get_running_app().rpc_connection, nickname, password)
        print(new_nickname)


class SubscribeOnRoomButton(Button):

    def subscribe_room(self, utxos_amount):
        chatlib.room_subscription(App.get_running_app().rpc_connection, str(App.get_running_app().active_room_id), utxos_amount)


class TrollboxCCApp(App):

    title = "OraclesCC Trollbox"

    active_room_id = ''

    messages = []

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

    def send_message(instance, inputid):
        new_message = chatlib.message_sending(App.get_running_app().rpc_connection, App.get_running_app().active_room_id, str(inputid.text))
        print(new_message)
        inputid.text = ''

    def callback_refresh_rooms(self, roomslist):
        roomslist.adapter.data = self.get_rooms_list()
        print("Room list succesfully refreshed")

    def on_press(self):
        print("I'm Working!")
        print(self.active_room_id)

    # checking selected chat room for new messages every 0.5 seconds
    message_updater = MessageUpdater()
    check_messages = Clock.schedule_interval(partial(MessageUpdater.messages_checker, message_updater), 0.5)
    check_messages()


if __name__ == "__main__":
    TrollboxCCApp().run()


