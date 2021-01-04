"""
TODO
"""
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
import requests

URL = 'https://www.instagram.com/'
URL_PROXY = 'https://free-proxy-list.net/'


def get_proxies():
    """
    TODO
    """
    while True:
        proxies = []
        approved_proxies = []
        errors = []
        html = requests.get(URL_PROXY).text
        soup = BeautifulSoup(html, 'lxml')

        trs = soup.find('table', id='proxylisttable').find_all('tr')[1:21]

        while not proxies:
            for tr in trs:
                tds = tr.find_all('td')
                if tds[-2].text.strip() == 'yes':
                    address = tds[0].text
                    port = tds[1].text
                    country = tds[3].text
                    data = {
                        'schema': 'https',
                        'address': address + ':' + port,
                        'country': country
                    }
                    proxies.append(data)

            if not proxies:
                print('---\tNo HTTPS proxies. Retry in 5 minutes.')
                sleep(300)
            elif len(proxies) < 2:
                print(f'---\tNot enough HTTPS proxies ({len(proxies)}).')
                print('\tRetry in 5 minutes.')
                proxies.clear()
                sleep(300)

        print(f'+++\tGot {len(proxies)} proxies - checking: ', end='')

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        for proxy in proxies:
            if len(options.arguments) > 1:
                options.arguments.pop()

            proxy = proxy['schema'] + ':' + proxy['address']
            options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Firefox(options=options)

            try:
                driver.get(URL)
                if driver.current_url == URL:
                    approved_proxies.append(proxy)
                    print('A', end='')
                else:
                    print('D', end='')
            except Exception as error:
                errors.append(error)
                print('-', end='')

            driver.quit()
        print()

        if approved_proxies:
            print(f'+++\tGot {len(approved_proxies)} approved proxies.')
            break
        print('---\tNone of proxes was approved.')
        print('\tErrors:')
        for e in errors:
            print('\t' + e)
        print('\tRetry in 5 min')
        sleep(300)

    return approved_proxies

def change_proxy(options, proxies):
    """
    TODO
    """
    options.arguments.pop()
    if len(proxies) < 2:
        print('---\tNeed new proxies.')
        return options
    options.arguments.pop()
    proxy = proxies.pop()
    options.add_argument(f'--proxy-server={proxy}')
    return options

if __name__ == '__main__':
    get_proxies()
