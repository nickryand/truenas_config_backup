#!/usr/bin/env python3
#
# Copyright 2021 Nick Downs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import socket
import requests

from datetime import datetime

from middlewared.client import Client
from middlewared.utils import sw_version

BACKUP_PATH = os.getenv("CLOUD_SYNC_PATH", os.getenv("BACKUP_PATH", "/tmp"))

# Set umask so all files are read/write only to the owner
os.umask(0o077)


def gen_filename():
    # The filename is generated similarly to how the webUI does it
    short_hostname = socket.gethostname().split('.')[0]
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{short_hostname}-{sw_version()}-{date}.tar"


def dispatch_job(client):
    args = {
        "secretseed": True,
        "pool_keys": True,
        "root_authorized_keys": True
    }
    result = client.call('core.download', 'config.save', [args], filename)

    return f"https://127.0.0.1/{result[1]}"


def download_backup(url):
    resp = requests.post(url, stream=True, verify=False)

    os.makedirs(BACKUP_PATH, exist_ok=True)
    full_path = os.path.join(BACKUP_PATH, filename)

    print(f"Downloading backup to {full_path}")
    with open(full_path, 'wb') as fp:
        for chunk in resp.iter_content():
            fp.write(chunk)

    resp.close()
    print("config backup complete")


if __name__ == "__main__":
    client = Client()
    global filename
    filename = gen_filename()
    download_backup(dispatch_job(client))
