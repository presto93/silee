def josa(txt, josa):
    symbols = ['!', '?', '.', ',']
    for symbol in symbols:
        txt.replace(symbol, '')
    print(txt)
    print(type(txt))
    code = ord(txt[-1]) - 44032
    cho = 19
    jung = 21
    jong=28
    if ((code < 0) or (code > 11171)):
        return txt + josa
    if (code % 28 == 0):
        return txt + Josa_get(josa, False)
    else:
        return txt + Josa_get(josa, True)

def Josa_get (josa, jong):
    if (josa == '을' or josa == '를'):
        return '을' if jong else '를'
    if (josa == '은' or josa == '는'):
        return '은' if jong else '는'
    return '**'