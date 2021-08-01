"""
TODO
"""
import re
import json

import requests

JS_PATTERN = r'static/bundles/es6/Consumer.js/\w*.js'
QUERY_HASH_PATTERN = r'profilePosts\.byUserId\.get[^,]+,queryId:"\w+"'
INTERNAL_DATA_PATTERN = r'window._sharedData\s=\s.+?;</script>'


def data_from_html(html):
    """
    TODO
    """
    media = {}

    match = re.search(INTERNAL_DATA_PATTERN, html).group()
    match = match.lstrip('window._sharedData= ').rstrip(';</script>')
    dict_data = json.loads(match)

    try:
        user = dict_data['entry_data']['ProfilePage'][0]['graphql']['user']
        profile_id = user['id']

        page = user['edge_owner_to_timeline_media']
        end_cursor = page['page_info']['end_cursor']
        has_next_page = page['page_info']['has_next_page']
        edges = page['edges']

        for edge in edges:
            slideshow = edge['node'].get('edge_sidecar_to_children')

            if slideshow:
                slideshow_edges = slideshow.get('edges')
                for slideshow_edge in slideshow_edges:
                    if slideshow_edge['node']['is_video']:
                        obj = {
                            slideshow_edge['node']['video_url']: 'mp4'}
                    else:
                        obj = {
                            slideshow_edge['node']['display_url']: 'jpg'}
                    media.update(obj)
            else:
                if edge['node']['is_video']:
                    obj = {edge['node']['video_url']: 'mp4'}
                else:
                    obj = {edge['node']['display_url']: 'jpg'}
                media.update(obj)
    except KeyError:
        # LOGGING TODO
        return {}

    return {
        'profile_id': profile_id,
        'has_next_page': has_next_page,
        'end_cursor': end_cursor,
        'media': media
    }


def data_from_ajax(dict_data):
    """
    TODO
    """
    media = {}

    try:
        page = dict_data['data']['user']['edge_owner_to_timeline_media']
        end_cursor = page['page_info']['end_cursor']
        has_next_page = page['page_info']['has_next_page']
        edges = page['edges']

        for edge in edges:
            slideshow = edge['node'].get('edge_sidecar_to_children')

            if slideshow:
                slideshow_edges = slideshow.get('edges')
                for slideshow_edge in slideshow_edges:
                    if slideshow_edge['node']['is_video']:
                        obj = {
                            slideshow_edge['node']['video_url']: 'mp4'}
                    else:
                        obj = {
                            slideshow_edge['node']['display_url']: 'jpg'}
                    media.update(obj)
            else:
                if edge['node']['is_video']:
                    obj = {edge['node']['video_url']: 'mp4'}
                else:
                    obj = {edge['node']['display_url']: 'jpg'}
                media.update(obj)
    except KeyError:
        # LOGGING TODO
        return {}

    return {
        'has_next_page': has_next_page,
        'end_cursor': end_cursor,
        'media': media
    }


def query_hash(html):
    """
    TODO
    """
    qhash = ''
    try:
        match = re.search(JS_PATTERN, html).group()
        script = requests.get('https://www.instagram.com/' + match).text
        match = re.search(QUERY_HASH_PATTERN, script).group()
        qhash = match.split('"')[-2]
    except AttributeError:
        # LOGGING TODO
        pass
    return qhash
