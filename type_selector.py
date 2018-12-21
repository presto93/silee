recommand_word = ['심심', '재미있는', '할일', '재밌는']
def get_content_type(text):
    text = text.lower()
    if 'ebook' in text or '이북' in text or 'e북' in text:
        return 'ebook'
    if '만화' in text:
        return 'comic'
    if '소설' in text or '장르' in text:
        return 'novel'
    if '영화' in text or '무비' in text:
        return 'movie'
    if '방송' in text or 'tv' in text or '드라마' in text or '예능' in text or '티비' in text or '텔레비' in text:
        return 'broadcasting'
    if '도움' in text or 'help' in text or '도와' in text or '모르겠' in text:
        return 'faq'
    if '전부' in text or '전체' in text or 'all' in text or '아무거나' in text:
        return 'all'
    return 'all'

def get_display_type(text):
    text = text.lower()
    if 'top10' in text or '탑탠' in text or '탑10' in text or '탑텐' in text or '인기' in text or '순위' in text or 'top텐' in text:
        return 'top'
    if '신간' in text or "new" in text or '최신' in text:
        return 'new'
    if text[:2] == '검색':
        return 'find'
    if '심심' in text or '재미있는' in text or '할일' in text or '재밌는':
        return 'recom'
    return 'none'

def get_element(type, display_type):
    if display_type == 'top':
        if type == 'ebook' or type == 'comic' or type == 'novel':
            return 'bstop10_list'
        if type == 'movie' or type == 'broadcasting':
            return 'tvtop10_list'

    if display_type == 'new':
        if type == 'ebook' or type == 'comic' or type == 'novel':
            return 'lst_thum_wrap'
        if type == 'movie' or type == 'broadcasting':
            return 'lst_thum_wrap'
    else:
        return None
