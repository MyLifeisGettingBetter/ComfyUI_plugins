#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time

from frp_conn import start_frpc
from image_generate import generate, upload_image
import json

if __name__=="__main__":
    proxy = start_frpc()

    with open("workflow_api.json", 'r', encoding='utf-8') as f:
        prompt = json.load(f)

    start = time.time()

    image_path = "./upload.png"
    upload_info = upload_image(proxy.subdomain, image_path)
    prompt["10"]["inputs"]["image"] = upload_info["name"]

    print(f"upload cost time:{time.time() - start}")
    start = time.time()

    images = generate(proxy.subdomain, prompt)
    print(f"upload cost time:{time.time() - start}")

    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io

            image = Image.open(io.BytesIO(image_data))
            image.save(str(node_id) + ".png")



    # input_images = ["20231116180824 (5) (1).jpg", "20-face_ex (2) (1) (1).png", "013a6f5c00e229a801209252dbb93a.jpg@1280w_1l_2o_100sh (2) (2).jpg", "dage0 (1).jpg"]
    # for i in range(len(input_images)):
    #     prompt["10"]["inputs"]["image"] = input_images[i]
    #     print(prompt)
    #     print("\n\n")
    #
    #     images = generate(proxy.subdomain, prompt)
    #
    #     for node_id in images:
    #         for image_data in images[node_id]:
    #             from PIL import Image
    #             import io
    #
    #             image = Image.open(io.BytesIO(image_data))
    #             image.save(str(node_id) + ".png")


    proxy.stop()
    proxy.clear_log()