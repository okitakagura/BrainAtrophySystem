# coding=utf-8
import matplotlib
from matplotlib import pylab as plt
import nibabel as nib
from nibabel.viewers import OrthoSlicer3D

file = 'nii/sub_002_brain_FLIRT.nii'  # 你的nii或者nii.gz文件路径
img = nib.load(file)

print(img)
print(img.header)  # 输出nii的头文件

width, height, queue = img.dataobj.shape

OrthoSlicer3D(img.dataobj).show()

num = 1
for i in range(0, queue):
    img_arr = img.dataobj[:, i:, ]
    plt.subplot(5, 4, num)
    plt.imshow(img_arr, cmap='gray')
    num += 1

plt.show()
