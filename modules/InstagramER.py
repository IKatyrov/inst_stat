import json
import requests

class InstagramER:
    def __init__(self, headers=None, proxy=None, cookies=None):
        # Инициализация заголовков
        self.__headers = headers
        # Инициализация прокси
        self.__proxy = proxy
        # Инициализация куки
        self.__cookies = cookies
    def __get_user_info(self, url):
        # Получение данных пользователя, в т.ч. посты
        user_info = requests.get(url, headers=self.__headers, proxies=self.__proxy, params={"__a": 1})
        # Если сервер ответил
        if user_info.status_code == 200:
            # Получение JSON-ответ
            json_info = user_info.text
            # Десертализация JSON в словарь
            return json.loads(json_info)
    def __get_count_of_subscribers(self, user_info):
        # Из словаря с данными возврат
        return user_info["graphql"]["user"]["edge_followed_by"]["count"]
    def __get_summary_likes_and_comments(self, user_info):
        # Счётчик комментариев
        count_of_comments = 0
        # Счётчик лайков
        count_of_likes = 0
        # Со скольки постов сбор статистики
        count_of_posts = len(user_info["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"])
        # Обход в цикле все посты
        for key in user_info["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]:
            # Суммирование количество комментариев поста к общему счётчику
            count_of_comments += key["node"]["edge_media_to_comment"]["count"]
            # Суммирование количество лайков поста к общему счётчику
            count_of_likes += key["node"]["edge_liked_by"]["count"]
        # Суммирование среднего количество лайков и среднего количества комментариев у одного поста
        return (count_of_comments / count_of_posts) + (count_of_likes / count_of_posts)
    def get(self, url):
        # Получение информацию о пользователей
        user_info = self.__get_user_info(url)
        # Получение количество подписчиков
        count_of_subscribers = self.__get_count_of_subscribers(user_info)
        # Получение суммарное количество лайков и репостов у одного поста (в среднем)
        summary_likes_and_comments = self.__get_summary_likes_and_comments(user_info)
        # Определяем ER
        return summary_likes_and_comments / count_of_subscribers * 100