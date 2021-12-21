import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy
from instaparser.inst_pwd_login import inst_pwd, inst_login


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = '	https://www.instagram.com/accounts/login/ajax/'
    inst_login = inst_login
    inst_pwd = inst_pwd
    main_users = ['ai_machine_learning', 'thearchitectsdiaryin']
    inst_api_link = 'https://i.instagram.com/api/v1/friendships/'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf})


    def login(self, response: HtmlResponse):
        # print()
        j_data = response.json()
        if j_data.get('authenticated'):
            for user in self.main_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_parse,
                    cb_kwargs={'main_username': user}
                )

    def user_parse(self, response: HtmlResponse, main_username):
        main_user_id = self.fetch_user_id(response.text, main_username)
        variables = {'count': 12, 'max_id': 0, 'search_surface': 'follow_list_page'}
        friendships_type = ['followers', 'following']
        # url_posts = f'{self.inst_api_link}query_hash={self.posts_hash}&{urlencode(variables)}'
        for friend_type in friendships_type:
            friends = f'{self.inst_api_link}{main_user_id}/{friend_type}/?&{urlencode(variables)}'
            yield scrapy.Request(friends,
                                 method='GET',
                                 callback=self.user_friends_parse,
                                 headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                 cb_kwargs={'main_username': main_username,
                                            'main_user_id': main_user_id,
                                            'friend_type': friend_type,
                                            'variables': deepcopy(variables)}
                                 )

    def user_friends_parse(self, response: HtmlResponse, main_username, main_user_id, friend_type, variables):
        j_data = response.json()
        users = j_data.get('users')
        for user in users:
            item = InstaparserItem(
                main_username=main_username,
                main_user_id=main_user_id,
                user_id=user.get('pk'),
                username=user.get('username'),
                full_name=user.get('full_name'),
                photo=user.get('profile_pic_url'),
                friend_type=friend_type,
            )
            yield item

        if j_data.get('big_list'):
            variables['max_id'] += 12
            friends = f'{self.inst_api_link}{main_user_id}/{friend_type}/?&{urlencode(variables)}'
            yield scrapy.Request(friends,
                                 method='GET',
                                 callback=self.user_friends_parse,
                                 headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                 cb_kwargs={'main_username': main_username,
                                            'main_user_id': main_user_id,
                                            'friend_type': friend_type,
                                            'variables': deepcopy(variables)}
                                 )


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')