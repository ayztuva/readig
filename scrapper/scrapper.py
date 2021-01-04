"""
TODO
"""
import json

import requests
from selenium import webdriver

from tools.proxy import get_proxies, change_proxy
from tools.getter import data_from_ajax, data_from_html, query_hash

JSON_URL = 'https://www.instagram.com/graphql/query/'
URL = 'https://www.instagram.com/graphql/query/'




def main():
    """
    Main function
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    proxies = get_proxies()

    profile_url = input('Profile URL: ')

    driver = webdriver.Firefox(options=options)

    driver.get(profile_url)




    with open('profiles.txt') as file:
        for url in file:
            media = []
            
            driver.get(url)
            html = driver.page_source
            username = url.rstrip('/\n').split('/')[-1]

            print(f'Scrapping media from {username}')

            # Get data from HTML
            data_html = data_from_html(html)
            media.extend(data_html['media'])

            # Get data from AJAX
            profile_id = data['profile_id']
            qhash = query_hash(html)
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
                response = requests.get(JSON_URL, params=params)
                container = response.json()
                data = data_from_ajax(container)
                media.extend(data['media'])

            with open(f'profiles/{username}.txt', 'w') as f:
                for url in media:
                    f.write(url+'\n')

    print('Done.')
    driver.quit()


if __name__ == '__main__':
    main()
