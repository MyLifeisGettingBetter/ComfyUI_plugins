#!/user/bin/env python3
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import socket
import threading

async def post_request():
    async with aiohttp.ClientSession(trust_env=True) as session:
        url = "http://127.0.0.1:8080/manager/wangtu"
        headers = {"Content-type": "application/json; charset=utf-8"}
        data = {"name":"zhangtao", "token":"this is the new"}
        params = {"i":66, "version":"1.0", "token_input":"token", "haha":"haha"}
        async with session.post(url, json=data, headers=headers, params=params) as resp:
            print(resp.url)
            if resp.status == 200 and resp.headers.get('Content-Type') == 'application/json; charset=utf-8':
                print(f"client status: {resp.status}")
                text = await resp.text(encoding='utf-8')
                print("response text: " + text)
            else:
                print("response error: " + str(resp.status))



if __name__ == "__main__":
    start_serve()
