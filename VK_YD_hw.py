import requests
import json

tk_vk_or = 'токен вк'
tk_yd_or = 'токен яндекс'

photos_info = {}


class Vk:
    url_vk = 'http://api.vk.com/method/'

    def __init__(self, tk_vk, version):
        self.tk_vk = tk_vk
        self.version = version
        self.params = {
            'access_token': self.tk_vk,
            'v': self.version
        }

    def vk_photos(self, page_id):
        photos_url = self.url_vk + 'photos.get'
        params = {
            'owner_id': page_id,
            'album_id': 'profile',
            'extended': '1',
        }
        response = requests.get(photos_url, params={**self.params, **params})
        if response.status_code == 200:
            print('Информафия о фото получена')
            for i in response.json()['response']['items']:
                like = str(i['likes']['count'])
                size = i['sizes'][-1]
                like_date = like + '_' + str(i['date'])
                if like not in photos_info:
                    photos_info[like] = size
                elif like in photos_info:
                    photos_info[like_date] = size
            print('У пользователя:', len(photos_info), 'фото')
        else:
            print('Ошибка:', response.status_code)


class Yd:
    url_yd = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token
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
            print('Папка', name_folder, 'создана')
        elif response.status_code == 409:
            print('Папка для загрузки была создана ранее')
        else:
            print('Ошибка при создании папки:', response.status_code)

    def up_photos_only_like(self, files, name_folder):
        url_upload = self.url_yd + '/upload'
        self.new_folder(name_folder)
        for k, v in files.items():
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

    def up_photos_like_date(self, files, name_folder, num_photos=5):
        url_upload = self.url_yd + '/upload'
        self.new_folder(name_folder)
        a = 0
        for k, v in files.items():
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
                a += 1
                if a == num_photos:
                    break
            else:
                print('Фото', name, 'не было сохранено на Диск. Ошибка:', response.status_code)

    def add_json(self, name_file):
        with open(name_file, 'w') as f:
            json.dump(self.photo_list, f, ensure_ascii=False, indent=2)
            print('Информация записана в файл:', name_file)

    def upload_files(self, files, name_folder, num_photos=5, name_file='info_photos.json'):
        if num_photos > len(photos_info):
            print('Будет загружено только', len(photos_info), 'фото')
            self.up_photos_only_like(files=files, name_folder=name_folder)
            self.add_json(name_file=name_file)
        elif num_photos <= len(photos_info):
            print('Будет загружено', num_photos, 'фото')
            self.up_photos_like_date(files=files, name_folder=name_folder, num_photos=num_photos)
            self.add_json(name_file=name_file)


vk_page = Vk(tk_vk_or, '5.130')
vk_page.vk_photos('ID')

y = Yd(tk_yd_or)
y.upload_files(photos_info, 'Название папки')
