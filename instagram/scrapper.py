
from bs4 import BeautifulSoup

STORY_IMAGE_PATTERN = ('i1HvM',)
STORY_VIDEO_PATTERN = ('OFkrO',)
POST_IMAGE_PATTERN = ()
POST_VIDEO_PATTERN = ()


class Scrapper:
    """Scrapper: scrapes media from page html"""

    def __init__(self):
        self.__sip = STORY_IMAGE_PATTERN
        self.__svp = STORY_VIDEO_PATTERN
        self.__pip = POST_IMAGE_PATTERN
        self.__pvp = POST_VIDEO_PATTERN

    def get_story_media(self, html):
        soup = BeautifulSoup(html, 'lxml')
        media = soup.find('img', class_=self.__sip)
        if media:
            srcset = media.get('srcset')
            media_url = srcset.split()[0]
            return media_url

        media = soup.find('video', class_=self.__svp)
        if media:
            source = media.find('source')
            media_url = source.get('src')
            return media_url
        raise ValueError('Story pattern error: wrong img classes')
