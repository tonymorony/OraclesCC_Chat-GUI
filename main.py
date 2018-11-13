from kivy.app import App
from kivy.config import Config
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from functools import partial
from bitcoin.core import CoreMainParams
import bitcoin


Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')
Config.set('kivy', 'window_icon', 'favicon.ico')

import rpclib
import chatlib
import bitcoinrpc
import ast
from bitcoin.wallet import P2PKHBitcoinAddress
from bitcoin.core import x
from datetime import datetime

class CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
'SECRET_KEY': 188}

bitcoin.params = CoinParams

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
            # getting oraclesinfo for active room
            oracles_info = rpclib.oracles_info(App.get_running_app().rpc_connection, App.get_running_app().active_room_id)
            if App.get_running_app().active_room_id == '':
                print("Seems messages grabbing works")
                break
            else:
            # flushing it to not print previous messages
                baton_returned = {}
            # getting batons to print on each iteration
                data_to_print = {}
            # getting dictionary with current batontxid for each publisher
                for entry in oracles_info["registered"]:
                    baton_returned[entry["publisher"]] = entry["batontxid"]
            # updating batons for all publishers in app array
                for publisher in baton_returned:
                    if publisher in App.get_running_app().current_baton:
            # if publisher already here updating baton and adding it to print queue
                        if baton_returned[publisher] != App.get_running_app().current_baton[publisher]:
                            App.get_running_app().current_baton[publisher] = baton_returned[publisher]
                            try:
                                data_to_print[publisher] = rpclib.oracles_samples(App.get_running_app().rpc_connection, App.get_running_app().active_room_id, baton_returned[publisher], "1")['samples'][0][0]
                            except IndexError:
                                break
            # if baton is the same as before there is nothing to update
                        else:
                            break
            # if publisher not here adding it with latest baton and adding baton to print queue
                    else:
                        App.get_running_app().current_baton[publisher] = baton_returned[publisher]
                        try:
                            data_to_print[publisher] = rpclib.oracles_samples(App.get_running_app().rpc_connection, App.get_running_app().active_room_id, baton_returned[publisher], "1")['samples'][0][0]
                        except IndexError:
                            break
            # finally printing messages
            try:
                for publisher in data_to_print:
                    message_list = ast.literal_eval(data_to_print[publisher].replace('\r','\\r').replace('\n','\\n'))
                    kvsearch_result = rpclib.kvsearch(App.get_running_app().rpc_connection, publisher)
                    if 'value' in kvsearch_result:
                        addr = str(P2PKHBitcoinAddress.from_pubkey(x(publisher)))
                        signature = kvsearch_result['value'][:88]
                        value = kvsearch_result['value'][88:]
                        verifymessage_result = rpclib.verifymessage(App.get_running_app().rpc_connection, addr, signature, value)
                        if verifymessage_result:
                            message_to_print = datetime.utcfromtimestamp(message_list[0]).strftime('%D %H:%M') + '[' + kvsearch_result['value'][88:] + '-' + publisher[0:10] + ']:' + message_list[1]
                        else:
                            message_to_print = 'IMPROPER SIGNATURE' + datetime.utcfromtimestamp(message_list[0]).strftime('%D %H:%M') + '[' + kvsearch_result['value'][88:] + '-' + publisher[0:10] + ']:' + message_list[1]
                    else:
                        message_to_print = datetime.utcfromtimestamp(message_list[0]).strftime('%D %H:%M') + '[' + publisher[0:10] + ']:' + message_list[1]
                    App.get_running_app().messages.append(message_to_print)
                    App.get_running_app().root.ids.messagesview.adapter.data = App.get_running_app().messages
                break
            except bitcoinrpc.authproxy.JSONRPCException as e:
                print(App.get_running_app().active_room_id)
                print(e)
                break

class CreateRoomButton(Button):

    def create_room(self, room_name, room_description):

        secret_room_description = "DCHAT " + room_description
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

    #key: publisher, value: batontxid
    current_baton = {}

    while True:
        try:
            rpc_connection = rpclib.rpc_connect("user1199437057", "passd8b8eab1a089da0b0cf4b309d35064503ae6ffd28b122c6443e0b09ffa70166c7c", 17205)
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

    # checking selected chat room for new messages every 0.5 seconds
    message_updater = MessageUpdater()
    check_messages = Clock.schedule_interval(partial(MessageUpdater.messages_checker, message_updater), 0.5)
    check_messages()


if __name__ == "__main__":
    TrollboxCCApp().run()


