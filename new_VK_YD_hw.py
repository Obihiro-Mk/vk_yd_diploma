from datetime import datetime
import requests
import json


class Vk:
    url_vk = 'http://api.vk.com/method/'

    def __init__(self, tk_vk_in, version='5.130'):
        self.tk_vk_in = tk_vk_in
        self.version = version
        self.params = {
            'access_token': self.tk_vk_in,
            'v': self.version
        }

    def get_users(self):
        page_id = input(str('Введите id: '))
        users_url = self.url_vk + 'users.get'
        params = {
            'user_ids': page_id
        }
        response = requests.get(users_url, params={**self.params, **params}).json()['response'][0]['id']
        return response

    def vk_photos(self):
        photos_info = {}
        page_id = self.get_users()
        count_photo = input('Какое количество фото загрузить?: ')
        photos_url = self.url_vk + 'photos.get'
        params = {
            'owner_id': page_id,
            'album_id': 'profile',
            'extended': '1',
            'count': count_photo,
        }
        response = requests.get(photos_url, params={**self.params, **params})
        if response.status_code == 200:
            for i in response.json()['response']['items']:
                like = str(i['likes']['count'])
                size = i['sizes'][-1]
                ts = datetime.utcfromtimestamp(int(i['date'])).strftime('%Y-%m-%d')
                like_date = like + '_' + str(ts)
                if like not in photos_info:
                    photos_info[like] = size
                elif like in photos_info:
                    photos_info[like_date] = size
            if int(count_photo) > len(photos_info):
                print('Информафия только о', len(photos_info), 'фото получена')
            else:
                print('Информафия о', count_photo, 'фото получена')
        else:
            print('Ошибка:', response.status_code)
        return photos_info


class Yd:
    url_yd = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, vk_token):
        self.token = token
        self.vk = Vk(vk_token)
        self.photo_list = []

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def new_folder(self, name_folder):
        headers = self.get_headers()
        params = {'path': name_folder, "overwrite": "true"}
        response = requests.put(self.url_yd, headers=headers, params=params)
        if response.status_code == 201:
            print('Папка', name_folder, 'создана на диске')
        elif response.status_code == 409:
            print('Папка для загрузки была создана ранее')
        else:
            print('Ошибка при создании папки:', response.status_code)

    def add_json(self, name_file):
        with open(name_file, 'w') as f:
            json.dump(self.photo_list, f, ensure_ascii=False, indent=2)
            print('Информация записана в файл:', name_file)

    def up_photos(self, name_folder, name_file='info_photos.json'):
        url_upload = self.url_yd + '/upload'
        self.new_folder(name_folder)
        photos_info = self.vk.vk_photos()
        for k, v in photos_info.items():
            photo_dict = {}
            url_save_vk = v['url']
            headers = self.get_headers()
            name = k + '.jpg'
            path = name_folder + '/' + name
            params = {'url': url_save_vk, 'path': path}
            response = requests.post(url_upload, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 202:
                print('Фото', name, 'сохранено на Диск')
                photo_dict['file name'] = name
                photo_dict['size'] = v['type']
                self.photo_list.append(photo_dict)
            else:
                print('Фото', name, 'не было сохранено на Диск. Ошибка:', response.status_code)
        self.add_json(name_file=name_file)


tk_vk = 'Токен вк'
tk_yd = 'Токен яндекс'
y = Yd(tk_yd, tk_vk)
y.up_photos('Название папки')
