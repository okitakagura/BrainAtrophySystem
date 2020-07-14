import SimpleITK
from scipy import misc as misc
import os
import numpy as np


def load_img(mhd_file, save_path):
    print(mhd_file)
    itk_img = SimpleITK.ReadImage(mhd_file)
    img_list = SimpleITK.GetArrayFromImage(itk_img)
    img_list_x = np.transpose(img_list, [1, 0, 2])
    img_list_y = np.transpose(img_list, [2, 0, 1])
    # print(save_path + '/ct_')
    mhd = os.path.basename(mhd_file)[:-4]
    dir_path = save_path + '/' + mhd
    print(dir_path)
    if os.path.isdir(dir_path):
        return img_list.shape[0]
    else:
        os.mkdir(dir_path)
        os.mkdir(os.path.join(dir_path, "0"))
        os.mkdir(os.path.join(dir_path, "1"))
        os.mkdir(os.path.join(dir_path, "2"))
    for i in range(img_list.shape[0]):
        img = img_list[i]
        misc.imsave(dir_path + '/0/ct_' + str(i) + '.png', img)

    for i in range(img_list_x.shape[0]):
        img = img_list_x[i]
        img = img[::-1]
        misc.imsave(dir_path + '/1/ct_' + str(i) + '.png', img)

    for i in range(img_list_y.shape[0]):
        img = img_list_y[i]
        img = img[::-1]
        misc.imsave(dir_path + '/2/ct_' + str(i) + '.png', img)
    return img_list.shape[0]


def load_nodules(mhd_file):
    print(mhd_file)
    # do something
