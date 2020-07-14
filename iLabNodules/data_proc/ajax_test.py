# -*- coding: utf-8 -*-

from django.http import JsonResponse
import os
from ..settings import BASE_DIR


def ajax_list(request):
    a = range(100)
    return JsonResponse(a, safe=False)


def ajax_dict(request):
    res_json = {}
    if request.method == 'GET':
        cnt = request.GET['cnt']
        res_json['cnt'] = cnt
        cnt = int(cnt)
        mhd = request.GET['value']
        if mhd:
            mhd = mhd[:-4]
            # path = os.path.join(BASE_DIR, 'index/static/image/' + mhd + '/' + request.GET['ca'] + '/ct_' + str(cnt) + '.png')
            path = os.path.join(BASE_DIR, 'index/static/image/' + mhd + '/' + request.GET['ca'] + '/' + str(cnt) + '.png')
            print(path)
            if os.path.isfile(path):
                res_json['path'] = 'image/' + mhd + '/' + request.GET['ca'] + '/' + str(cnt) + '.png'

    return JsonResponse(res_json)
