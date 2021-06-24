import re
from datetime import datetime

import requests


def get_site_metrics(site):
    now = datetime.now()

    request_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("request_time={}".format(request_time))
    try:
        b = requests.get(site)
        b.raise_for_status()

        http_response_time = b.elapsed.total_seconds()
        status_code = b.status_code
        search_text = re.search("<title>(.*?)</title>", b.text)

        grouped_text = ''
        if search_text:
            grouped_text = search_text.group(1)

        return {
            "request_time": request_time,
            "type": "SUCCESS",
            "site_url": site,
            "response_time_sec": http_response_time,
            "status_code": status_code,
            "regex_search": grouped_text
        }
    except requests.exceptions.RequestException as e:
        return {
            "request_time": request_time,
            "type": "ERROR",
            "site_url": site,
            "exception_type": type(e).__name__
        }
