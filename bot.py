from dotenv import dotenv_values

from instagram.view import Viewer
from instagram.scrapper import Scrapper

env = dotenv_values('.env')
USERNAME = env.get('USERNAME')
PASSWORD = env.get('PASSWORD')


v = Viewer(USERNAME, PASSWORD)
v.login()

# html = v.get_story_html('')
# scrapper = Scrapper()
# url = scrapper.get_story_media(html)
# print(url)

v.close_driver()
