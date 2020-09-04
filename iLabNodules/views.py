# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import common
from index import models
import json
import time
import os
import shutil
import nibabel as nib
import imageio
import datetime
from . import mainreport
from threading import Thread
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

def register(request):
    # 注册页面
    return render(request, 'register.html', {})

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
                # for i in range(z):
                #     silce = img_fdata[i, :, :]
                #     imageio.imwrite(os.path.join(img_f_path, '{}.png'.format(i)), silce)

                img_file = './index/static/image/'
                img_f_path = os.path.join(img_file, fname)
                img_res_path = os.path.join('./index/static/img/', fname + '_result')
                if not os.path.exists(img_f_path) and not os.path.exists(img_res_path):
                    os.mkdir(img_f_path)
                    os.mkdir(img_res_path)
                    # 创建nii对应的图像的文件夹
                    # if not os.path.exists(img_f_path):
                    #     os.mkdir(img_f_path)  # 新建文件夹
                    for i in range(3):
                        os.mkdir(os.path.join(img_f_path, str(i)))
                    # 开始转换为图像0
                    (x, y, z) = img.shape
                    for i in range(z):  # z是图像的序列
                        silce = img_fdata[i, :, :]  # 选择哪个方向的切片都可以
                        imageio.imwrite(os.path.join(img_f_path, '0/{}.png'.format(i)), silce)
                        # 保存图像
                    # 开始转换为图像1
                    (x, y, z) = img.shape
                    for i in range(z):  # z是图像的序列
                        silce = img_fdata[:, i, :]  # 选择哪个方向的切片都可以
                        imageio.imwrite(os.path.join(img_f_path, '1/{}.png'.format(i)), silce)
                        # 保存图像
                    # 开始转换为图像2
                    (x, y, z) = img.shape
                    for i in range(z):  # z是图像的序列
                        silce = img_fdata[:, :, i]  # 选择哪个方向的切片都可以
                        imageio.imwrite(os.path.join(img_f_path, '2/{}.png'.format(i)), silce)
                        # 保存图像
            imagefile = models.ImageFile.objects.filter(filename=filename).first()
            if imagefile:
                return HttpResponse(json.dumps(2))
            else:
                models.ImageFile.objects.create(filename=filename, addtime=times).save()
            thr = Thread(target=mainreport.main, args=(img_path, img_f_path, img_res_path))
            thr.start()
        return HttpResponse(json.dumps(1))
@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        filename = request.POST.get('del_filename')
        addressname = request.POST.get('del_filename')
        filename = filename+'.nii'
        imagefile2 = models.ImageFile.objects.filter(filename=filename).first()
        if imagefile2:
            models.ImageFile.objects.filter(filename=filename).delete()
            imagefile = models.ImageFile.objects.filter(filename=filename).first()
            if imagefile:
                return HttpResponse(json.dumps(2))
            else:
                shutil.rmtree('./index/static/img/'+addressname)
                shutil.rmtree('./index/static/img/' + addressname+'_result')
                os.remove('./index/static/img/' + addressname+'.nii')
                shutil.rmtree('./index/static/image/' + addressname)
                return HttpResponse(json.dumps(1))
        else:
            return HttpResponse(json.dumps(3))

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
    filename = data
    file1 = "image/" + filename + "/30.png"
    file2 = "image/" + filename + "/45.png"
    file3 = "image/" + filename + "/50.png"
    context = {'data': [], 'purl': []}

    try:
        f = open('./index/static/img/' + filename + '_result' + '/V', 'r')
        V = f.read()
        f.close()
        V = V.split('\n')
        V = [float(V[0]), float(V[1]), float(V[2])]
        V_sum = sum(V)
        percent_p2 = V[0] / V_sum * 100
        percent_p3 = V[1] / V_sum * 100
        percent_p4 = V[2] / V_sum * 100
    except:
        context = {'data':[{"name": "数据正在加载中", "absolute": '请稍后刷新', "relative": '', "percent": ''}], 'purl': []}
        return render(request, 'print.html', context)

    # 脑数据在这里定义：
    context = {'data': [
        {"name": "颅内总体积", "absolute": '%.3f' % V_sum, "relative": 100, "percent": 9},
        {"name": "脑脊液", "absolute": '%.3f' % V[0], "relative": '%.1f' % percent_p2,
         "percent": int((percent_p2 * 10 - int(percent_p2 * 10)) * 10)},
        {"name": "灰质", "absolute": '%.3f' % V[1], "relative": '%.1f' % percent_p3,
         "percent": int((percent_p3 * 10 - int(percent_p3 * 10)) * 10)},
        {"name": "白质", "absolute": '%.3f' % V[2], "relative": '%.1f' % percent_p4,
         "percent": int((percent_p4 * 10 - int(percent_p4 * 10)) * 10)}
    ],
        "purl": [file1, file2, file3]
    }

    return render(request, 'print.html', context)
    # eng = matlab.engine.start_matlab()
    # result_V = eng.KFCM_S(data_src, nargout=3)
    # CSF_V = result_V[0]
    # GM_V = result_V[1]
    # WM_V = result_V[2]
    # whole_V = CSF_V + GM_V + WM_V
    # whole_V =  float(format(whole_V, '.3f'))
    # CSF_rela = CSF_V / whole_V * 100.00
    # GM_rela = GM_V / whole_V * 100.00
    # WM_rela = WM_V / whole_V *100.00
    # CSF_rela = format(CSF_rela, '.3f')
    # GM_rela = format(GM_rela, '.3f')
    # WM_rela = format(WM_rela, '.3f')
    # context = {'data': [
    #     {"name": "颅内总体积", "absolute": whole_V, "relative": 100, "percent": 0},
    #     {"name": "脑脊液", "absolute": CSF_V, "relative": CSF_rela, "percent": 0},
    #     {"name": "脑灰质", "absolute": GM_V, "relative": GM_rela, "percent": 0},
    #     {"name": "脑白质", "absolute": WM_V, "relative": WM_rela, "percent": 0}
    # ],
    #     "purl": [img0_src,
    #              img1_src,
    #              img2_src
    #              ]
    # }

