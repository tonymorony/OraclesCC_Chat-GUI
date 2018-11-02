import rpclib
import time
from kivy.app import App


#getting list of specific CHAT rooms from oracleslist
def get_chat_rooms(rpc_connection):

    start_time = time.time()
    oracles_list = rpclib.oracles_list(rpc_connection)
    chat_rooms_list = []
    for oracle_txid in oracles_list:
        oraclesinfo_result = rpclib.oracles_info(rpc_connection, oracle_txid)
        description = oraclesinfo_result['description']
        name = oraclesinfo_result['name']
        if description[0:4] == 'CHAT':
            chat_room = '[' + name + ': ' + description[5:] + ']: ' + oracle_txid
            chat_rooms_list.append(chat_room)
    print("--- %s seconds ---" % (time.time() - start_time))
    return chat_rooms_list


# return latest batontxid from all publishers
def get_latest_batontxids(rpc_connection, oracletxid):

    oraclesinfo_result = rpclib.oracles_info(rpc_connection, oracletxid)
    latest_batontxids = {}
    # fill "latest_batontxids" dictionary with publisher:batontxid data
    for i in oraclesinfo_result['registered']:
        latest_batontxids[i['publisher']] = i['batontxid']
    return latest_batontxids


def set_nickname(rpc_connection, username, password):

    address = rpclib.getaccountaddress(rpc_connection, "")
    pubkey = rpclib.validateaddress(rpc_connection,address)["pubkey"]

    signmessage_result = rpclib.signmessage(rpc_connection, address, username)
    value = signmessage_result + username

    kvupdate_result = rpclib.kvupdate(rpc_connection, pubkey, value, 100, password)
    print(kvupdate_result)
    nickname = kvupdate_result
    print(nickname)
    return nickname


def room_subscription(rpc_connection, roomtxid, utxos_amount):

    address = rpclib.getaccountaddress(rpc_connection, "")
    validation = rpclib.validateaddress(rpc_connection,address)
    pubkey = validation["pubkey"]
    print(utxos_amount)
    try:
        registration_hex = rpclib.oracles_register(rpc_connection, roomtxid, "10000")
        registration_txid = rpclib.sendrawtransaction(rpc_connection, registration_hex["hex"])
    except Exception as e:
        print(e)
    else:
        print(registration_txid)

    for utxo in range(int(utxos_amount)):
        try:
            subscription_hex = rpclib.oracles_subscribe(rpc_connection, roomtxid, pubkey, "1")
            subscription_txid = rpclib.sendrawtransaction(rpc_connection, subscription_hex["hex"])
            print(subscription_txid)
        except Exception as e:
            print(e)


