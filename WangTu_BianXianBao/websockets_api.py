#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint
import random
import sys

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import requests

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def upload_image(filepath, overwrite=False):
    try:
        files = {'image': open(filepath, 'rb')}
        data = {'overwrite': str(overwrite).lower()}
        response = requests.post("http://{}/upload/image".format(server_address), files=files, data=data)
        return response.json()
    except Exception as e:
        print(e)

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    request_info = queue_prompt(prompt)
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
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]

    #仅输出感兴趣SaveImage节点编号的图片
    # final_images = {}
    # save_image_index = '101'
    # final_image = history['outputs'][save_image_index]
    # if "images" in final_image:
    #     images_output = []
    #     for image in final_image['images']:
    #         image_data = get_image(image['filename'], image['subfolder'], image['type'])
    #         images_output.append(image_data)
    #     final_images[save_image_index] = images_output

    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            if images_output:
                output_images[node_id] = images_output

    return output_images


upload_info = upload_image('20231116180824.jpg', overwrite=False)
print(upload_info['name'])
with open("workflow_api.json", 'r') as f:
    prompt = json.load(f)
prompt["3"]["inputs"]["seed"] = random.randint(0, sys.maxsize)
prompt["20"]["inputs"]["image"] = upload_info['name']
ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images= get_images(ws, prompt)

for node_id in images:
    for image_data in images[node_id]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.save(str(node_id) + ".png")

