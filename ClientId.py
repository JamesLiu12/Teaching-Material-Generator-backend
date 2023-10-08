import utils
import json
import os

client_id_to_time = {}
timeout_second = 60


def check_client_id(client_id):
    if client_id in client_id_to_time.keys():
        return False
    client_id_to_time[client_id] = utils.get_system_time()
    return True


def delete_timeout_clients():
    client_id_to_delete = []
    for client_id in client_id_to_time.keys():
        current_time = utils.get_system_time()
        time_dif = utils.get_time_dif(current_time, client_id_to_time[client_id])
        if time_dif > timeout_second:
            client_id_to_delete.append(client_id)
            try:
                os.remove(os.path.join("json/client", f"{client_id}.json"))
            except:
                pass
    for client_id in client_id_to_delete:
        client_id_to_time.pop(client_id)


def update_client_time(client_id):
    client_id_to_time[client_id] = utils.get_system_time()
