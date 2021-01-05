"""
TODO
"""
from time import sleep

from bs4 import BeautifulSoup
import requests

URL = 'https://www.instagram.com/'
URL_PROXY = 'https://free-proxy-list.net/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_proxies():
    """
    TODO
    """
    while True:
        proxies = []
        approved_proxies = []
        errors = []

        while not proxies:
            html = requests.get(URL_PROXY).text
            soup = BeautifulSoup(html, 'lxml')
            trs = soup.find('table', id='proxylisttable').find_all('tr')[1:21]
            for tr in trs:
                tds = tr.find_all('td')
                if tds[-2].text.strip() == 'yes':
                    address = tds[0].text
                    port = tds[1].text
                    data = {
                        'schema': 'https',
                        'address': address + ':' + port
                    }
                    proxies.append(data)

            if not proxies:
                print('---\tNo HTTPS proxies. Retry in 3 minutes.')
                sleep(180)
            elif len(proxies) < 2:
                print(f'---\tNot enough HTTPS proxies ({len(proxies)}).')
                print('\tRetry in 3 minutes.')
                proxies.clear()
                sleep(180)

        print(f'+++\tGot {len(proxies)} proxies - checking: ', end='')

        for proxy in proxies:
            try:
                response = requests.get(
                    URL,
                    proxies=proxy,
                    headers=HEADERS
                )
                if response.status_code == 200:
                    approved_proxies.append(proxy)
                    print('A', end=' ')
                else:
                    print('D', end=' ')
            except Exception as error:
                errors.append(error)
                print('D', end=' ')
        print()

        if approved_proxies:
            print(f'+++\tGot {len(approved_proxies)} approved proxies.')
            break
        print('---\tNone of proxes was approved.')
        print('\tErrors:')
        for error in errors:
            print('\t' + error)
        print('\tRetry in 3 min')
        sleep(180)

    return approved_proxies

def change_proxy(options, proxies):
    """
    TODO
    """
    if len(proxies) < 2:
        print('---\tNeed new proxies.')
        return options
    proxies.pop()
    options.arguments.pop()
    p = proxies[-1]
    proxy = p['schema'] + ':' + p['address']
    options.add_argument(f'--proxy-server={proxy}')
    return options

if __name__ == '__main__':
    get_proxies()
