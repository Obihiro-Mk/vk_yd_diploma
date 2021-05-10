from pprint import pprint

import requests


# def vk_photos(id):
#     url = 'http://api.vk.com/method/photos.get'
#     params = {
#         'owner_id': id,
#         'album_id': 'profile',
#         'extended': '1',
#         'access_token': tk_vk,
#         'v': '5.130'
#     }
#     res = requests.get(url, params=params)
#     for i in res.json()['response']['items']:
#         l = i['likes']['count']
#         s = i['sizes']
#         print(l, s)
tk_yd_or = ''


class Yd:
    url_yd = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def new_folder(self, name_folder):
        headers = self.get_headers()
        params = {'path': name_folder, "overwrite": "true"}
        response = requests.put(self.url_yd, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def pr_f(self):
        folder = self.new_folder('ppp')
        print(folder['href'])


# def upload_files(self, files, name_folder, num_photos=5):
#     url_upload = self.url_yd + '/upload'
#     self.new_folder(name_folder)
#     if num_photos > len(photos_info):
#         for k, v in files.items():
#             url_save_vk = v['url']
#             headers = self.get_headers()
#             path = name_folder + '/' + k + '.jpg'
#             params = {'url': url_save_vk, 'path': path}
#             response = requests.post(url_upload, headers=headers, params=params)
#             response.raise_for_status()
#             if response.status_code == 202:
#                 print('Фото', k, 'сохранено на Диск')
#         print('Загружено только', len(photos_info), 'фото')
#     elif num_photos <= len(photos_info):
#         a = 0
#         for k, v in files.items():
#             url_save_vk = v['url']
#             headers = self.get_headers()
#             path = name_folder + '/' + k + '.jpg'
#             params = {'url': url_save_vk, 'path': path}
#             response = requests.post(url_upload, headers=headers, params=params)
#             response.raise_for_status()
#             if response.status_code == 202:
#                 print('Фото', k, 'сохранено на Диск')
#                 a += 1
#                 if a == num_photos:
#                     break
#     else:
#         print('Ошибка при загрузке')

y = Yd(tk_yd_or)
y.pr_f()
# y.new_folder('test_folder')