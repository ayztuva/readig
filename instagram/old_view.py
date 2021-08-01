import json
import os
import tempfile
from urllib.request import urlretrieve
from zipfile import ZipFile

import requests
from selenium import webdriver

from tools.getter import data_from_ajax, data_from_html, query_hash
from tools.proxy import Proxy

JSON_URL = ('https://www.instagram.com/graphql/query/' +
            '?query_hash={}&variables={}')
URL = 'https://www.instagram.com/graphql/query/'
TMP_URL = 'https://www.instagram.com/'
SUCCESS_RESPONSE = 200
HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': '(iPhone; iOS 7.0.4; Scale/2.00)',
}


def main():
    proxies = get_proxies()
    media = {}
    proxy = proxies.pop()

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument(
        f"--proxy-server={proxy['schema']}:{proxy['address']}")
    driver = webdriver.Firefox(options=options)

    profile_url = input('\tProfile URL: ')
    username = profile_url.rstrip('/\n').split('/')[-1]

    # TODO
    # Somehow need to check here if status code isn't 200
    while True:
        driver.get(profile_url)
        html = driver.page_source
        driver.quit()

        print(f'\tScrapping {username}:', end='\t')

        # Get data from HTML
        data = data_from_html(html)
        if data:
            media.update(data['media'])
            print('H', end=' ')
            break
        else:
            proxy = change_proxy(proxies)
            driver.quit()
            options.arguments.pop()
            options.add_argument(
                f"--proxy-server={proxy['schema']}:{proxy['address']}")
            driver = webdriver.Firefox(options=options)

    # Work data
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

        myproxy = {
            proxy['schema']: proxy['schema'] + '://' + proxy['address'],
        }
        response = requests.get(
            JSON_URL,
            params=params,
            proxies=myproxy,
            headers=HEADERS,
        )
        if response.status_code != SUCCESS_RESPONSE:
            proxy = change_proxy(proxies)
            myproxy = {
                proxy['schema']: proxy['schema'] + '://' + proxy['address'],
            }
            requests.get(TMP_URL, proxies=myproxy)
            continue

        try:
            container = response.json()
        except json.JSONDecodeError as error:
            print(f"\n---\tCan't extract JSON.\n\tError:{error}")
            print('\n---\tFailed.')
            break

        data = data_from_ajax(container)
        media.update(data['media'])
        print('*', end='')

    # Download recieved media and save in archive
    os.chdir(os.getcwd() + '/profiles')
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir:
        name = 0
        for key, value in media.items():
            if value == 'jpg':
                filename = f'{tmp_dir}/{name}.jpg'
            else:
                filename = f'{tmp_dir}/{name}.mp4'
            urlretrieve(key, filename)
            name += 1

        with ZipFile(username + '.zip', 'w') as zipf:
            for folder, _subfolders, files in os.walk(tmp_dir):
                for obj in files:
                    path = os.path.join(folder, obj)
                    zipf.write(path, os.path.basename(path))

    print('\n+++\tDone.')


if __name__ == '__main__':
    main()
