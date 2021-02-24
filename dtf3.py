import requests
import requests.auth
import urllib3
urllib3.disable_warnings()
import vk
import vk_api
from bs4 import BeautifulSoup
import time
#vk.logger.setLevel('DEBUG')
#  Получение токена (t) - https://vkhost.github.io/

#Пропишем функцию для парсинга названий статей и ссылок на них с главной страницы сайта:
def pars():
    #Здесь будет храниться список названий статей:
    list1 = []
    #Здесь будет храниться список ссылок на статьи:
    list2 = []
    #Здесь будет храниться название последней опубликованной статьи и ссылка на нее:
    list3 = [] 
    #Получаем URL главной страницы сайта, откуда будем брать статьи (главная страница):
    url = 'https://dtf.ru/'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('div', class_='news_item l-flex l-fa-baseline lm-block l-mv-9 lm-mv-8')
    for item in items:
        #Парсим все названия статей с сайта по классу 'announs_item':
        title = item.find('a').get_text(strip=True)
        #Парсим все ссылки на статьи с сайта по классу 'announs_item':
        href = item.find('a').get('href')
        list1.append(title)
        list2.append(href)
    list3.append(list1[0])
    list3.append(list2[0])
    return list3


#Организовываем цикл для автоматического постинга свежих статей в соощество Vk:
while True:
    #print(pars())
    list4 = pars()
    #Записываем в переменную lastpost последнюю опубликованную статью на сайте https://dtf.ru/
    lastpost = list4[0]
    print(lastpost)
    time.sleep(300)
    #Заново парсим названия статей и ссылки, чтобы проверить, появилась ли на сайте новая сатья:
    list4 = pars()
    
    if list4[0] != lastpost:
        # Авторизация через токен админа:
        t = ''
        session = vk_api.VkApi(token = t)
        vk_api = session.get_api() 
        # Атибуты нашего будущего поста вк:
        requestparams = {
                            'method': 'wall.post', 
                            'oauth': '1', 
                            'v': '5.126', 
                            'owner_id': '-120599126', # ID сообщества (со знаком -)
                            'from_group': '1', # 1 = запись от имени группы
                            'message': list4[0],
                            'attachments': list4[1] ,
                            #'publish_date': time1, - (time1 - время отложенной публикации)
                        } 
        #Публикуем на стену сообщества ссылку на свежую статью, если она появилась на сайте:
        vk_api.wall.post(**requestparams)
        time.sleep(10) 
