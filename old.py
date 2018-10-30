from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.focus import FocusBehavior
import rpclib
import chatlib

class TrollboxCCApp(App):


    def build(self):

        text = ""
        messages = ""
        rooms_list_text = ""

        #window_layout = BoxLayout(orientation="horizontal", padding=10)

        #chat_layout = BoxLayout(orientation="vertical", padding=10)
        #messaging_layout = BoxLayout(orientation="horizontal", padding=10, size_hint=(1, 0.2))
        #messages_display = Label(text=messages, text_size=(400, 500), halign="left", valign="top")
        #chats_display = BoxLayout(orientation="vertical", padding=10)
        #rooms_list = Label(text=rooms_list_text, text_size=(350, 500), halign="left", valign="top")
        #send_msg_button = Button(text="Send", size_hint=(0.2, 1))
        #create_room_button = Button(text="Create room", size_hint=(1, 0.1))
        #refresh_rooms_button = Button(text="Refresh rooms", size_hint=(1, 0.1))
        #text_input = TextInput(text=text)
        text_input.focus = True

        oracles_list = rpclib.oracles_list(rpc_connection)

        def on_text(instance, value):
            self.text = value

        text_input.bind(text=on_text)

        def callback_send(instance):
            messages_display.text = messages_display.text + self.text + "\n"
            text_input.text = ""

        def callback_create_room(instance):
            rooms_list.text = rooms_list.text + "Blah\n"

        def callback_refresh_rooms(instance):
            chat_rooms_list = chatlib.get_chat_rooms(rpc_connection, oracles_list)
            rooms_list.text = str(chat_rooms_list)

        refresh_rooms_button.bind(on_press=callback_refresh_rooms)
        send_msg_button.bind(on_press=callback_send)
        create_room_button.bind(on_press=callback_create_room)

      #  chats_display.add_widget(rooms_list)
      #  chats_display.add_widget(create_room_button)
      #  chats_display.add_widget(refresh_rooms_button)

        #messaging_layout.add_widget(text_input)
        #messaging_layout.add_widget(send_msg_button)

       #chat_layout.add_widget(messages_display)
        #chat_layout.add_widget(messaging_layout)

        #window_layout.add_widget(chats_display)
       # window_layout.add_widget(chat_layout)

        return window_layout


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
