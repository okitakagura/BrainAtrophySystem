# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import common
from index import models
import json
import time
import os
import nibabel as nib
import imageio
import datetime
@csrf_exempt
def index(request):
    # 判断用户是否登录
    filenames = ''
    if request.method == 'POST':
        type = request.POST["type"]
        username = request.POST["username"]
        password = request.POST["password"]
        if(type == 'login'):
            user_res = models.UserInfo.objects.filter(user=username).first()
            if user_res:
                if user_res.password == password:
                    request.session['username'] = username
                    res = 1
                else:
                    res = 3
            else:
                res = 2
            return HttpResponse(json.dumps(res))
        elif type == 'register':
            email = request.POST["email"]
            phone = request.POST["phone"]
            user_resa = models.UserInfo.objects.filter(user=username).first()
            if user_resa:
                res = 2
            else:
                models.UserInfo.objects.create(user=username, password=password, email=email, phone=phone).save()
                res = 1
            return HttpResponse(json.dumps(res))
    if request.method == 'GET':
        filenames = request.GET.get('filename', default='')
    context = {}
    nodules = {}

    data = [nodules]

    ImageArr = models.ImageFile.objects.all()
    list = []
    for Image in ImageArr:
        arr = {}
        arr['id'] = Image.id
        filename = Image.filename
        arr['filename'] = filename[:-4]
        arr['addtime'] = Image.addtime
        list.append(arr)
    context['nodules'] = data
    context['ImageArr'] = list
    context['filenames'] = filenames
    return render(request, 'index.html', context)

def login(request):
    # 登陆页面
    return render(request, 'login.html', {})
@csrf_exempt
def home(request):
    starttime = ''
    endtime = ''
    if request.method == 'POST':
        starttime = request.POST["starttime"]
        endtime = request.POST["endtime"]
        if not starttime:
            starttime = datetime.datetime.now()
        if not endtime:
            endtime = datetime.datetime.now()
        ImageArr = models.ImageFile.objects.filter(addtime__gte=starttime,addtime__lte=endtime)
    else:
        ImageArr = models.ImageFile.objects.all()
    list = []
    for Image in ImageArr:
        arr = {}
        arr['id'] = Image.id
        filename = Image.filename
        arr['filename'] = filename[:-4]
        arr['addtime'] = Image.addtime
        list.append(arr)
    context = {}
    context['imageArr'] = list
    context['starttime'] = starttime
    context['endtime'] = endtime
    return render(request, 'home.html', context)

@common.auth
def logout(request):
    request.session.flush()
    return redirect('login')

@common.auth
def updatePwd(request):
    return render(request, 'updatePwd.html', {})

@csrf_exempt
def update_pwd(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = request.session['username']
        user_res = models.UserInfo.objects.filter(user=user).first()
        password_files = user_res.password
        if password1 != password_files:
            return HttpResponse(json.dumps(2))
        obj = models.UserInfo.objects.filter(id=user_res.id)[0]
        obj.password = password2
        obj.save()
        return HttpResponse(json.dumps(1))
    else:
        return HttpResponse(json.dumps(0))
@csrf_exempt
def uploadfile(request):
    if request.method == 'POST':
        filename = request.FILES.get('filename')
        times = datetime.datetime.now()
        if filename:
            file = "./index/static/img/"+filename.name
            with open(file, 'wb') as f:  # 新建1张图片 ，图片名称为 上传的文件名
                for temp in filename.chunks():  # 往图片添加图片信息
                    f.write(temp)
            if ".nii" in filename.name:
                file_name = filename.name
                img_path = os.path.join('./index/static/img/',file_name)

                img = nib.load(img_path)
                img_fdata = img.get_fdata()
                fname = file_name.replace('.nii', '')
                img_f_path = os.path.join('./index/static/img/', fname)
                if not os.path.exists(img_f_path):
                    os.mkdir(img_f_path)
                (x, y, z) = img.shape
                for i in range(z):
                    silce = img_fdata[i, :, :]
                    imageio.imwrite(os.path.join(img_f_path, '{}.png'.format(i)), silce)
            imagefile = models.ImageFile.objects.filter(filename=filename).first()
            if imagefile:
                return HttpResponse(json.dumps(2))
            else:
                models.ImageFile.objects.create(filename=filename, addtime=times).save()
        return HttpResponse(json.dumps(1))
def print_page1(request):
    '''
        报告打印页面
    '''
    data = request.GET["data"]
    filename = data
    file = "img\/"+filename+"\/25.png"
    context = {}
    # 脑数据在这里定义：
    context = {'data': [
        {"name": "颅内总体积", "absolute": 1243.532, "relative": 100, "percent": 9},
        {"name": "脑实质", "absolute": 868.715, "relative": 69.9, "percent": 4},
        {"name": "海马区", "absolute": 4.678, "relative": 0.376, "percent": 9},
        {"name": "杏仁核", "absolute": 2.162, "relative": 0.174, "percent": 0},
        {"name": "丘脑", "absolute": 10.572, "relative": 0.85, "percent": 22},
        {"name": "尾状核", "absolute": 5.638, "relative": 0.453, "percent": 55},
        {"name": "壳核", "absolute": 7.904, "relative": 0.636, "percent": 34},
        {"name": "苍白球", "absolute": 2.563, "relative": 0.206, "percent": 54},
        {"name": "伏隔核", "absolute": 0.655, "relative": 0.0527, "percent": 5},
        {"name": "中脑", "absolute": 4.709, "relative": 0.379, "percent": 46},
        {"name": "桥脑", "absolute": 11.700, "relative": 0.941, "percent": 39},
        {"name": "延脑", "absolute": 3.221, "relative": 0.259, "percent": 7},
        {"name": "小脑上脚", "absolute": 0.165, "relative": 0.0133, "percent": 73},
        {"name": "小脑", "absolute": 114.360, "relative": 9.2, "percent": 73}
    ],
        "purl": [file]
    }

    return render(request, 'print.html', context)


def print_page(request):
    '''
        报告打印页面
    '''
    data = request.GET["data"]
    context = {}

    if data == 'sub_001_brain_FLIRT':
        # 脑数据在这里定义：
        context = {'data': [
            {"name": "颅内总体积", "absolute": 1243.444, "relative": 100, "percent": 9},
            {"name": "海马区", "absolute": 4.678, "relative": 0.378, "percent": 11},
            {"name": "杏仁核", "absolute": 2.169, "relative": 0.181, "percent": 1}
        ],
            "purl": [r"image\sub_003_brain_FLIRT\0\25.png",
                     r"image\sub_003_brain_FLIRT\1\25.png",
                     r"image\sub_003_brain_FLIRT\2\25.png"
                     ]
        }
    if data == 'sub_002_brain_FLIRT':
        # 脑数据在这里定义：
        context = {'data': [
            {"name": "颅内总体积", "absolute": 1246.532, "relative": 100, "percent": 9},
            {"name": "海马区", "absolute": 4.386, "relative": 0.379, "percent": 10},
            {"name": "杏仁核", "absolute": 2.167, "relative": 0.163, "percent": 0}
        ],
            "purl": [r"image\sub_003_brain_FLIRT\0\25.png",
                     r"image\sub_003_brain_FLIRT\1\25.png",
                     r"image\sub_003_brain_FLIRT\2\25.png"
                     ]
        }
    if data == 'sub_003_brain_FLIRT':
        # 脑数据在这里定义：
        context = {'data': [
            {"name": "颅内总体积", "absolute": 1243.542, "relative": 100, "percent": 9},
            {"name": "海马区", "absolute": 4.678, "relative": 0.376, "percent": 11},
            {"name": "杏仁核", "absolute": 2.163, "relative": 0.175, "percent": 0}
        ],
            "purl": [r"image\sub_003_brain_FLIRT\0\25.png",
                     r"image\sub_003_brain_FLIRT\1\25.png",
                     r"image\sub_003_brain_FLIRT\2\25.png"
                     ]
        }
    if data == 'sub_004_brain_FLIRT':
        context = {'data': [
            {"name": "颅内总体积", "absolute": 1239.582, "relative": 100, "percent": 8},
            {"name": "海马区", "absolute": 5.834, "relative": 0.386, "percent": 10},
            {"name": "杏仁核", "absolute": 2.162, "relative": 0.174, "percent": 0}
        ],
            "purl": [r"image\sub_004_brain_FLIRT\0\25.png",
                     r"image\sub_004_brain_FLIRT\1\25.png",
                     r"image\sub_004_brain_FLIRT\2\25.png"
                     ]
        }
    if data == 'sub_005_brain_FLIRT':
        context = {'data': [
            {"name": "颅内总体积", "absolute": 1225.592, "relative": 100, "percent": 10},
            {"name": "海马区", "absolute": 4.652, "relative": 0.388, "percent": 12},
            {"name": "杏仁核", "absolute": 2.162, "relative": 0.174, "percent": 0}

        ],
            "purl": [r"image\sub_005_brain_FLIRT\0\25.png",
                     r"image\sub_005_brain_FLIRT\1\25.png",
                     r"image\sub_005_brain_FLIRT\2\25.png"
                     ]
        }
    return render(request, 'print.html', context)
