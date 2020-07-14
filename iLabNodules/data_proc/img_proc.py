# -*- coding: utf-8 -*-

from django.http import JsonResponse
from . import load
from ..settings import BASE_DIR
import os


def load_img(request):
    res = {}
    file_name = request.GET['src']
    mhd_file = os.path.join(BASE_DIR, "data/" + str(file_name))
    if os.path.isfile(mhd_file):
        save_path = os.path.join(BASE_DIR, "index/static/image")
        cnt = load.load_img(mhd_file, save_path)
        res['max_cnt'] = cnt
        print(request.GET['src'])

    return JsonResponse(res)


def load_nodules(request):
    file_name = request.GET['src']
    mhd_file = os.path.join(BASE_DIR, "data/" + str(file_name))
    res = {}
    if file_name == "sub_001_brain_FLIRT.mhd":
        res = {'nodules': [
            {'x': 100, 'y': 9, 'z': 1234.444, 'name': '颅内总体积'},
            {'x': 0.181, 'y': 1, 'z': 2.169, 'name': '杏仁核'},
            {'x': 0.378, 'y': 11, 'z': 4.678, 'name': '海马区'}
        ]}
    if file_name == "sub_002_brain_FLIRT.mhd":
        res = {'nodules': [
            {'x': 100, 'y': 9, 'z': 1246.532, 'name': '颅内总体积'},
            {'x': 0.163, 'y': 0, 'z': 2.167, 'name': '杏仁核'},
            {'x': 0.379, 'y': 10, 'z': 4.386, 'name': '海马区'}
        ]}
    if file_name == "sub_003_brain_FLIRT.mhd":
        res = {'nodules': [
            {'x': 100, 'y': 9, 'z': 1234.542, 'name': '颅内总体积'},
            {'x': 0.175, 'y': 0, 'z': 2.163, 'name': '杏仁核'},
            {'x': 0.376, 'y': 11, 'z': 4.678, 'name': '海马区'}
        ]}
    if file_name == "sub_004_brain_FLIRT.mhd":
        res = {'nodules': [
            {'x': 100, 'y': 8, 'z': 1239.582, 'name': '颅内总体积'},
            {'x': 0.177, 'y': 0, 'z': 2.162, 'name': '杏仁核'},
            {'x': 0.386, 'y': 10, 'z': 5.834, 'name': '海马区'}
        ]}
    if file_name == "sub_005_brain_FLIRT.mhd":
        res = {'nodules': [
            {'x': 100, 'y': 10, 'z': 1225.592, 'name': '颅内总体积'},
            {'x': 0.182, 'y': 0, 'z': 2.170, 'name': '杏仁核'},
            {'x': 0.388, 'y': 12, 'z': 4.652, 'name': '海马区'}
        ]}
    return JsonResponse(res)
