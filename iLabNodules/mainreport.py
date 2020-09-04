import nibabel as nib
from matplotlib import pylab as plt
import numpy as np
import sys
import os
import imageio
from . import MyKFCM_S
from nibabel.viewers import OrthoSlicer3D
np.set_printoptions(threshold=np.inf)

def XieBeniInverted(U,expo,center,data):
    dist=np.sum(pow(U,expo)*pow(distfcm(center,data),2))
    minimum=sys.maxsize
    for i in range(0,center.shape[0]-1):
        if(center.shape[1]==1):
            minimumAux=(distfcmfp(np.array([center[i]]),center[i+1:,])**2).min()
        else:
            minimumAux=(distfcmfp(center[i],center[i+1:,])**2).min()
        if(minimum>minimumAux):
            minimum=minimumAux
    xieBeni=dist/(data.shape[0]*minimum)
    return xieBeni

def distfcm(center,data):
    out=np.zeros((center.shape[0],data.shape[0]))
    for k in range(0,center.shape[0]): #对每一个聚类中心
        out[k] = pow((((data - np.ones((data.shape[0], 1))*center[k])**2).T).sum(axis=0), 0.5)
    return out

def distfcmfp(center,data):
    out = np.zeros((center.shape[0], data.shape[0]))
    if(center.shape[1]>1):
        for k in range (0,center.shape[0]):
            out[k] = pow((((data - np.ones((data.shape[0], 1))*center[k])**2).T).sum(axis=0), 0.5)
    else:
        for k in range(0,center.shape[0]):
            out[k]=abs(center[k]-data).T
    return out

def main(filepath,dirpath_ori,dirpath_res):
    img=nib.load(filepath)#装载nii数据
    w,h,q=img.dataobj.shape#获取.nii文件的三个维度,一般1,2维是图像维度,第3维是切片
    v_p1=0
    v_p2=0
    v_p3=0
    v_p4=0
    n_start=0
    n_end=79
    for slicenum in range(n_start,n_end):
        data_load=img.dataobj[:,:,slicenum]
        data_load=data_load.T#旋转90度
        data2=data_load
        a=data2.shape#计算图像矩阵的大小
        data=np.reshape(data2,(-1,1),'F')#转换为列向量
        data=data.astype(np.float64)
        data_n=data.shape#求出data的第一维(rows)数,即样本个数和求出data的第二维(columns)数，即特征值长度
        options = [2,150,1e-5,0] # 指定隶属度矩阵的的模糊指数，算法迭代次数，迭代终止条件等
        cluster_n = 4 #指定类别数
        expo = options[0]#隶属度矩阵U的指数
        max_iter = options[1]#最大迭代次数
        min_impro = options[2]#隶属度最小变化量, 迭代终止条件
        display = options[3]#每次迭代是否输出信息标志
        alfa = 1.5
        while True:
            try:
                U,center,obj_fcn=MyKFCM_S.MyKFCM_S(data_load,cluster_n,alfa,expo,max_iter,min_impro,display)
            except:
                continue
            break
        fm=pow(U,expo)
        V_pc=np.sum(fm)/data_n[0]
        V_xieben=XieBeniInverted(U,expo,center,data)

        #图像分割
        data=data.T
        wholeG=np.zeros(data.shape)
        maxU=U.max(0)
        x=[1,2,3,4]
        id=np.argsort(center,axis=0)
        center=np.sort(center,axis=0)
        x=id
        count = []
        result = []
        for k in range(0,cluster_n):
            indexk=(U[k]==maxU)
            indexk = indexk.astype(np.int)
            count.append(sum(indexk))
            Ik=indexk*data
            Ik=Ik.reshape(a,order='F')
            result.append(Ik)#result{k}记录第Ｋ类中的像素及其位置信息
            for j in range(0,indexk.shape[0]):
                if(indexk[j]==1):
                    wholeG[0,j]=indexk[j]*(x[k,0]+1)
        wholeG=wholeG.reshape(a,order='F')#将向量转化为a*b大小的矩阵
        imageio.imwrite(os.path.join(dirpath_res, '{}.png'.format(slicenum)), wholeG)
        imageio.imwrite(os.path.join(dirpath_ori, '{}.png'.format(slicenum)), data_load)
        s_p2=count[x[1,0]]*0.04
        s_p3=count[x[2,0]]*0.04
        s_p4=count[x[3,0]]*0.04
        if (slicenum==n_start or slicenum==n_end-1):
            v_p2=v_p2+s_p2
            v_p3=v_p3+s_p3
            v_p4=v_p4+s_p4
        else:
            v_p2=v_p2+2*s_p2
            v_p3=v_p3+2*s_p3
            v_p4=v_p4+2*s_p4
    V_p2=v_p2*0.2/2
    V_p3=v_p3*0.2/2
    V_p4=v_p4*0.2/2
    f = open(os.path.join(dirpath_res+'/', 'V'),'w')
    f.write(str(V_p2) + '\n' + str(V_p3) + '\n' + str(V_p4))
    f.close()
    return
