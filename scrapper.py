"""
TODO
"""
import json

import requests
from selenium import webdriver

from tools.proxy import get_proxies, change_proxy
from tools.getter import data_from_ajax, data_from_html, query_hash

JSON_URL = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={}'
URL = 'https://www.instagram.com/graphql/query/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}



def reset_driver(driver, options, proxies):
    """
    Change driver options
    """
    url = driver.current_url
    driver.close()
    change_proxy(options, proxies)

    if not proxies:
        print('---\tNo proxiest. Getting new.')
        proxies.extend(get_proxies())

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver

def main():
    """
    Scrapper
    """
    proxies = get_proxies()
    media = []

    proxy = proxies[-1]['schema'] + ':' + proxies[-1]['address']
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Firefox(options=options)

    profile_url = input('\tProfile URL: ')
    username = profile_url.rstrip('/\n').split('/')[-1]

    driver.get(profile_url)
    html = driver.page_source

    print(f'\tScrapping {username}:', end='\t')

    # Get data from HTML
    data = data_from_html(html)
    media.extend(data['media'])

    # Needed data
    qhash = query_hash(html)
    profile_id = data['profile_id']

    # Get data from AJAX
    while data['has_next_page']:
        variables = {
            'id': profile_id,
            'first': 12,
            'after': data['end_cursor']
        }
        params = {
            'query_hash': qhash,
            'variables': json.dumps(variables)
        }

        response = requests.get(
            JSON_URL,
            params=params,
            proxies=proxies[-1],
            headers=HEADERS
        )

        try:
            container = response.json()
        except json.JSONDecodeError as error:
            print(f"\n---\tCan't extract JSON.\n\tError:{error}")
            print('\n---\tFailed.')
            break

        data = data_from_ajax(container)
        media.extend(data['media'])
        print('*', end='')

    with open(f'profiles/{username}.txt', 'w') as file:
        for url in media:
            file.write(url+'\n')

    print('\n+++\tDone.')
    driver.quit()


if __name__ == '__main__':
    main()
