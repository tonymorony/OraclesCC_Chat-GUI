import rpclib

#getting list of specific CHAT rooms from oracleslist
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

#def set_user_name():


#def create_chat_room():
# have to auto-register

# return latest batontxid from all publishers
def get_latest_batontxids(rpc_connection, oracletxid):
    oraclesinfo_result = rpclib.oracles_info(rpc_connection, oracletxid)
    latest_batontxids = {}
    # fill "latest_batontxids" dictionary with publisher:batontxid data
    for i in oraclesinfo_result['registered']:
        latest_batontxids[i['publisher']] = i['batontxid']
    return latest_batontxids