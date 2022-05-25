# reminder: after 4.8k+ requests google will ask you to fill a captcha if you are not using proxy

import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


"""
URL: your form url # must be response URL, sample is provided
REFERER: take by filling a response
COOKIE: take by filling a response
DATA: fill a form lol

PROXYS: you can provide proxies also.
SPEED: change this value to increase the speed of spam. (500> not allowed)
SPAMMY: change this to increase spam count
"""

SPEED = 63 
SPAMMY = 100000 

URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfoemQg90qTmA4ps9yh-YU46_9xDcMzBILr-wSnPpyXVr9BLA/formResponse'

DATA = 'entry.2005620554=kushal&entry.1045781291=kushal%40gmail.com&entry.1166974658=1234567890&fvv=1&partialResponse=%5Bnull%2Cnull%2C%224688203165610129769%22%5D&pageHistory=0&fbzx=4688203165610129769'

REFERER = 'https://docs.google.com/forms/d/e/1FAIpQLSfoemQg90qTmA4ps9yh-YU46_9xDcMzBILr-wSnPpyXVr9BLA/viewform?fbzx=4688203165610129769'

COOKIE = 'S=spreadsheet_forms=_MWW_iXuve4ymMWEWsadrXL3MQ9E2nZslrqG0IpKaOI; NID=511=r7jrQT0RP2pXBPytn9JdONT8-Ji7XGUoITz5bgqxO0oDdIRIIKUm2t9qU7u-ddviv-HnYzCf6ePo5I24kVq8ivmRbgThX-Bn5JQHwSSYGzmI5BwaVErPulCdnkiwF7cUOlXBtBHuKMtaYE-SRAWQ7IV80t0oi-hHubIQYcX1bbY'


HEADER = {
    'Host': 'docs.google.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://docs.google.com',
    'Referer': REFERER,
    'Cookie': COOKIE,
    'Upgrade-Insecure-Requests':'1'
    }

PROXYS = []




def trouble():
    try:
        if len(PROXYS) > 0: 
            proxy = PROXYS[random.choice([x for x in range(len(PROXYS))])]
            r = requests.post(URL, proxies={'http':proxy, 'https':proxy}, data=DATA, headers=HEADER)
        else:
            r = requests.post(URL, data=DATA, headers=HEADER)
        return r
    except Exception as e:
        raise Exception (e)


if __name__ == "__main__":

    with ThreadPoolExecutor(SPEED=SPEED) as executor:
        future_calls = {executor.submit(trouble): count for count in range(SPAMMY)}

        for future in as_completed(future_calls):
            try:
                result = future.result()
                print('[-] {}'.format(result.status_code))
            except Exception as e:
                print('[!] {}'.format(e))
