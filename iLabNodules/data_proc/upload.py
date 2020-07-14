# -*- coding: utf-8 -*-
from django.http import HttpResponse
import os
from ..settings import BASE_DIR


def upload(request):
    print("parsing.")
    if not request.method == "POST":
        print("please use POST method!")
        return HttpResponse("please use POST method!")
    else:
        my_file = request.FILES.get("upload", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not my_file:
            print("No files for upload!")
            return HttpResponse("No files for upload!")
        else:
            # 打开特定的文件进行二进制的写操作
            destination = open(os.path.join(BASE_DIR, "data/" + str(my_file.name)), 'wb+')
            # 分块写入文件
            for chunk in my_file.chunks():
                destination.write(chunk)
            destination.close()
            print("upload suc! the file name is " + str(my_file.name))
            return HttpResponse("upload suc! the file name is " + str(my_file.name))
