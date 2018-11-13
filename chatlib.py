import rpclib
import time
import codecs
import sys
import codecs
import requests
import time
import bitcoin
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress
from bitcoin.core import x


class CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
'SECRET_KEY': 188}


bitcoin.params = CoinParams

#getting list of specific CHAT rooms from oracleslist
def get_chat_rooms(rpc_connection):

    start_time = time.time()
    oracles_list = rpclib.oracles_list(rpc_connection)
    chat_rooms_list = []
    for oracle_txid in oracles_list:
        oraclesinfo_result = rpclib.oracles_info(rpc_connection, oracle_txid)
        description = oraclesinfo_result['description']
        name = oraclesinfo_result['name']
        if description[0:5] == 'DCHAT':
            chat_room = '[' + name + ': ' + description[6:] + ']: ' + oracle_txid
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
    return kvupdate_result


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


def message_sending(rpc_connection, roomtxid, message_text):

    while True:
        message = "[" + str(int(time.time())) + " ,\"" + str(message_text) + "\"]"
        # convert message to hex
        rawhex = codecs.encode(message).hex()

        # get length in bytes of hex in decimal
        bytelen = int(len(rawhex) / int(2))
        hexlen = format(bytelen, 'x')

        # get length in big endian hex
        if bytelen < 16:
            bigend = "000" + str(hexlen)
        elif bytelen < 256:
            bigend = "00" + str(hexlen)
        elif bytelen < 4096:
            bigend = "0" + str(hexlen)
        elif bytelen < 65536:
            bigend = str(hexlen)
        else:
            print("message too large, must be less than 65536 characters")
            break

        # convert big endian length to little endian, append rawhex to little endian length
        lilend = bigend[2] + bigend[3] + bigend[0] + bigend[1]
        fullhex = lilend + rawhex

        # print(fullhex)
        oraclesdata_result = rpclib.oracles_data(rpc_connection, roomtxid, fullhex)
        # print(oraclesdata_result)
        result = oraclesdata_result['result']
        if result == 'error':
            print('ERROR:' + oraclesdata_result['error'] + ', try using oraclesregister if you have not already')
            break
        rawtx = oraclesdata_result['hex']

        sendrawtx_result = rpclib.sendrawtransaction(rpc_connection, rawtx)
        print(sendrawtx_result)
        return sendrawtx_result
