import rpclib

def get_chat_rooms(rpc_connection):

    oracles_list = rpclib.oracles_list(rpc_connection)
    chat_rooms_list = []
    for oracle_txid in oracles_list:
        oraclesinfo_result = rpclib.oracles_info(rpc_connection, oracle_txid)
        description = oraclesinfo_result['description']
        name = oraclesinfo_result['name']
        if description[0:4] == 'CHAT':
            chat_room = '[' + name + ': ' + description[5:] + ']: ' + oracle_txid
            chat_rooms_list.append(chat_room)
    return chat_rooms_list
