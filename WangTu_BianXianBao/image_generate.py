#!/user/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import json
import websocket
import urllib.request
import urllib.parse
import requests

def upload_image(proxy_name, filepath, overwrite=False):
    server_address = str(proxy_name) + ".zt.suaike.online:20000"
    try:
        files = {'image': open(filepath, 'rb')}
        data = {'overwrite': str(overwrite).lower()}
        response = requests.post("http://{}/upload/image".format(server_address), files=files, data=data)
        return response.json()
    except Exception as e:
        print(e)


def generate(proxy_name, prompt):
    server_address = str(proxy_name) + ".zt.suaike.online:20000"
    print(f"websocket for frps address: {server_address}")
    client_id = str(uuid.uuid4())
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, prompt, server_address, client_id)
    return images

def queue_prompt(prompt, server_address, client_id):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type, server_address):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id, server_address):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt, server_address, client_id):
    request_info = queue_prompt(prompt, server_address, client_id)
    prompt_id = request_info['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue
    history = get_history(prompt_id, server_address)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'], server_address)
                    images_output.append(image_data)
            if images_output:
                output_images[node_id] = images_output
    return output_images