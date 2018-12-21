import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
from urllib import parse
import type_selector as ts
import random
URL = 'https://nstore.naver.com/'
INTRO = "안녕하세요 NAVER N스토어 챗봇입니다.\n카테고리를 선택해주세요\nex) E북, 만화, 소설, 영화, 방송, 도움말, 검색"


def get_name(type):
    if type == 'ebook':
        return 'EBook'
    if type == 'comic':
        return '만화'
    if type == 'novel':
        return '장르소설'
    if type == 'movie':
        return '영화'
    if type == 'broadcasting':
        return '방송'


def get_author(info_list):
    author = ''
    for info in info_list:
        if '작가' in info.get_text():
            author = info.get_text()[3:]
        elif '주연' in info.get_text():
            author = info.get_text()[2:]
        elif '글' in info.get_text() or '그림' in info.get_text():
            author = info.get_text()[2:]
    return author


def get_title(title, type):
    if type == 'ebook' or type == 'comic' or type == 'novel':
        title = title.get_text().split()
        result = ''
        for t in title:
            result = result + t + ' '
        return result
    if type == 'broadcasting' or type == 'movie':
        title = title.get_text().strip()
        return title.replace('HD(1080)', '').replace('\n', '').replace('\t', '').replace('HD', '')


def get_synopsis(page, type):
    synopsis = ''
    try:
        synopsis = page.find_all('div', class_='_synopsis')
        synopsis = synopsis[-1].get_text().strip()

        length = len(synopsis)
        if (synopsis[length - 2: length] == '접기'):
            synopsis = synopsis[:length - 2]
        synopsis = synopsis.strip()
    except:
        try:
            synopsis = page.find_all('div', class_='end_dsc _open NE=a:mvi')
            length = len(synopsis)
            if (synopsis[length - 2: length] == '접기'):
                synopsis = synopsis[:length - 2]
        except:
            synopsis = page.find(
                'div', class_='end_dsc _close NE=a:mvi').get_text()
    return synopsis


def crawl_by_title(title, type):
    title = title.split(':')[-1].strip()
    title = title.split('/')[0]
    path = URL + 'search/search.nhn?t={}&q={}'.format(type, parse.quote(title.replace(' ', '+'), "utf-8"))
    print(path)
    soup = BeautifulSoup(urllib.request.urlopen(path).read(), "html.parser")
    lst_list = soup.find('ul', class_='lst_list')
    display_text = []
    if lst_list is None:
        return "검색 결과가 없습니다\n" + INTRO
    for li in lst_list.find_all('li'):
        try:
            next_path = URL + li.find('a')['href']
            detail = BeautifulSoup(urllib.request.urlopen(
                next_path).read(), "html.parser")
            detail_content = detail.find('div', id='content')
            # display_text.append(title)
            print(title)
            info_list = detail_content.find(
                'li', class_='info_lst').find_all('li')
            author = get_author(info_list)
            
            try:
                synopsis = detail.find_all('div', class_='_synopsis')
                display_text.append('제목 : {} / 작가 : {}'.format(title, author))
            except:
                synopsis = detail.find_all('div', class_='end_dsc _open NE=a:mvi')
                display_text.append('제목 : {} / 주연 : {}'.format(title.strip('-')[0:], author))
            

            synopsis = get_synopsis(detail, type)
            display_text.append(synopsis)
            display_text.append('')

        except:
            pass
    print(display_text)
    return display_text

def get_videos(ul):
    videos = []
    for li in ul:
        try:
            next_path = URL + li.find('a')['href']
            print(next_path)
            detail = BeautifulSoup(urllib.request.urlopen(next_path).read(), "html.parser")
            detail_content = detail.find('div', id='content')
            title = detail_content.find('h2')
            print(title)
            title = title.get_text().split()
            c_title = ''
            for t in title:

                c_title = c_title + t

            print(c_title.replace('HD(1080)','').replace('\n','').replace('\t','').replace('HD',''))
            info_list = detail_content.find('li', class_='info_lst').find_all('li')

            author = get_author(info_list)
            print(author)
            videos.append('제목 : {} / 주연 : {}'.format(c_title, author))
        except:
            pass
    return videos

def get_books(ul):
    books = []
    for li in ul:
        try:
            next_path = URL + li.find('a')['href']

            detail = BeautifulSoup(urllib.request.urlopen(next_path).read(), "html.parser")

            detail_content = detail.find('div', id='content')
            title = detail_content.find('h2')
            title = title.get_text().split()
            c_title = ''
            for t in title:
                c_title = c_title + t

            info_list = detail_content.find('li', class_='info_lst').find_all('li')

            author = get_author(info_list)
            books.append('제목 : {} / 작가 : {}'.format(c_title, author))
        except:
            pass
    return books

def crawl_news(text, type):
    
    url = URL + type + '/home.nhn'
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    display_text = []
    display_text.append("----- {} 신 간 -----".format(get_name(type)))
    lst_thum_wrap = soup.find('div', class_=ts.get_element(type, 'new'))
    ul = lst_thum_wrap.find_all('li')
    if type == 'ebook' or type == 'comic' or type == 'novel':
        ul = get_books(ul)
    if type == 'movie' or type == 'broadcasting':
        ul = get_videos(ul)
    for li in ul:
        display_text.append(li)
    return display_text


def crawl_top10(text, type):

    url = URL + type + '/home.nhn'
    print(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    display_text = []
    bstop10_list = soup.find('ul', class_=ts.get_element(type, 'top'))
    display_text.append("----- {} T O P  1 0 -----".format(get_name(type)))
    ul = bstop10_list.find_all('li')
    if type == 'ebook' or type == 'comic' or type == 'novel':
        ul = get_books(ul)
    if type == 'movie' or type == 'broadcasting':
        ul = get_videos(ul)
    for li in ul:
        display_text.append(li)
    return display_text


def get_random_one():
    type =['ebook', 'comic', 'novel', 'movie', 'broadcasting']
    type = type[random.randrange(0, 5)]

    url = URL + type + '/home.nhn'
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    bstop10_list = soup.find('ul', class_=ts.get_element(type, 'top'))
    title = bstop10_list.find_all('li')[random.randrange(0, 10)].find('a')['title']

    return '요즘 인기있는는 어떠세요?\n자세한 내용을 보려면 검색 입력하세요!'