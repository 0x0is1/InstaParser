import requests

class InstaParser:
    COUNT = 12
    APP_ID = 936619743392459
    def __init__(self, username):
        self.url = f'https://www.instagram.com/api/v1/feed/user/{username}/username/?count={self.COUNT}' 

    cookies = {
        'ds_user_id': '0'
    }

    headers = {
        'x-ig-app-id': str(APP_ID),
        'x-requested-with': 'XMLHttpRequest'
    }

    def fetch_posts(self, count: int=12, next_max_id:str=None):
        if count != 12:
            self.COUNT = count
        if next_max_id is not None:
            self.url = f'{self.url}&max_id={next_max_id}'
        response = requests.get(self.url, cookies=self.cookies, headers=self.headers, stream=True)
        return response.json()

    def get_postThumbnails(self, data:dict):
        next_max_id = data['next_max_id']
        count = data['num_results']
        more_available = data['more_available']
        container = {
            'max_id': next_max_id,
            'count': count,
            'more_available': more_available,
            'images': []
        }

        for item in data['items']:
            try:
                img_url = item['image_versions2']['candidates'][0]['url']
                container['images'].append(img_url)
            except KeyError:
                for subitem in item['carousel_media']:
                    img_url = subitem['image_versions2']['candidates'][0]['url']
                    container['images'].append(img_url)

        return container

    def get_postVideo(self, data:dict):
        count = data['num_results']
        more_available = data['more_available']
        next_max_id = None
        if more_available:
            next_max_id = data['next_max_id']
        container = {
            'max_id': next_max_id,
            'count': count,
            'more_available': more_available,
            'videos': []
        }

        for item in data['items']:
            try:
                img_url = item['video_versions'][0]['url']
                container['videos'].append(img_url)
            except KeyError:
                pass

        return container

    def get_userDetails(self, data:dict):
        user = data['user']
        return {
            "name": user["full_name"],
            "username": user["username"],
            "profile_picture": user["profile_pic_url"]
        }