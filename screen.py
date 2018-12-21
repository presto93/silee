import random
import josa

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

def recommand(type):
    type_list = ['EBook', '만화', '소설', '영화', '방송']
    if type == 'none' or type == 'all':
        return '무슨말인지 잘 모르겠어요. 오늘은 {} 어떠세요?'.format(type_list[random.randrange(0, 5)])
    else:
        type = get_name(type)
        flg = random.randrange(0, 3)
        if flg == 0:
            return "요즘 인기있는 {} 찾아드릴까요? '{} 순위 알려줘' 라고 말해보세요!".format(josa.josa(type, '을'), type)
        elif flg == 1:
            return "새로나온 {} 어떠세요? '최신{} 알려줘' 라고 말해보세요!".format(josa.josa(type, '은'), type)
