import hashlib,time
from django.http.response import JsonResponse

urls = {}
mykey = 'zjkassj32jk3iosakjas8928173kklas2'


def checkUrl():
    ctime = time.time()
    _urls = {**urls}
    for u, ct in _urls.items():
        if ctime - ct > 5:
            del urls[u]

def api_post_method(req):
    url = req.path
    checkUrl()
    auth_key, client_ctime = req.META['HTTP_AUTHKEY'].split('|')
    md5 = hashlib.md5()
    md5.update(bytes(mykey + client_ctime, encoding='utf8'))
    vaildition_key = md5.hexdigest()
    ctime = time.time()
    if ctime - 5 > float(client_ctime):
        return False
    if url in urls:
        return False
    else:
        if vaildition_key == auth_key:
            urls[url] = ctime
            return True
        elif vaildition_key != auth_key:
            return False

def authkey(func):
    def inner(req,*args,**kwargs):
        if api_post_method(req):
            return func(req,*args,**kwargs)
        else:
            return JsonResponse({'status':False,"msg":'auth failed'})
    return inner