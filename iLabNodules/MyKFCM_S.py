import numpy as np
from . import kmeans4
def MyKFCM_S(data_load,cluster_n,alfa,expo=2.0,max_iter=100,min_impro=1e-5,display=1):
#MyKFCM_S采用改进的结合邻域信息和核函数的模糊C均值对数据集data聚为cluster_n类
# 输入：
#   data_load   ---- 数据集
#   cluster_n     ---- 聚类数目
#   alfa  ---- 邻域信息权重
#   expo  ---- 隶属度矩阵U的指数，>1                  (缺省值: 2.0)
#   max_iter  ---- 最大迭代次数                           (缺省值: 100)
#   min_impro  ---- 隶属度最小变化量,迭代终止条件           (缺省值: 1e-5)
#   display  ---- 每次迭代是否输出信息标志                (缺省值: 1)
# 输出：
#   U           ---- 隶属度矩阵
#   center      ---- 聚类中心
#   obj_fcn     ---- 目标函数值
    data2=np.array(data_load)  #读入原始图像
    a,b=data2.shape  #图像矩阵的大小

    img1=np.array(data2)
    width=3;  #局部窗尺寸
    delta=(width-1)//2
    for i in range(delta,a-delta):
        for j in range(delta,b-delta):
            temp=data2[i-delta:i+delta+1,j-delta:j+delta+1]
            temp=np.sort(temp.flatten())
            img1[i][j]=temp[(np.max(temp.shape)+1)//2-1]

    data1=np.reshape(img1,(-1,1),'F')  #转化为列向量
    data1=data1.astype(np.float64)
    data=np.reshape(data2,(-1,1),'F')  #转化为列向量
    data=data.astype(np.float64)
    data_n=data.size  #求出样本个数

    obj_fcn=np.zeros((max_iter,1))  #初始化输出参数obj_fcn
    U = initfcm(cluster_n,data_n)  #初始化模糊分配矩阵,使U满足列上相加为1

    center=kmeans4.kmeans4(data_load)
    segma=estimateSegma(data)
    #初始化聚类中心：从样本数据点中任意选取cluster_n个样本作为聚类中心
    #当然如果采用某些先验知识选取中心或许能够达到加快稳定的效果，但目前不具备这功能

    #主要循环
    for i in range(0,max_iter):
        #在第k步循环中改变聚类中心ceneter,和分配函数U的隶属度值
        U,center,obj_fcn[i]=stepfcm(data,data1,center,U,cluster_n,expo,alfa,segma)
        if display :
            print('MyKFCM_S:Iteration count = %d, obj. fcn = %f'%(i,obj_fcn[i]))
        #终止条件判别
        if i>0:
            if abs(obj_fcn[i]-obj_fcn[i-1])<min_impro:
                break
    iter_n=i  #实际迭代次数
    obj_fcn=obj_fcn[:iter_n]
    return U,center,obj_fcn

def initfcm(cluster_n,data_n):
#初始化fcm的隶属度函数矩阵
# 输入:
#   cluster_n - --- 聚类中心个数
#   data_n - --- 样本点数
# 输出：
#   U - --- 初始化的隶属度矩阵

    U = np.random.random((cluster_n,data_n))
    col_sum=sum(U)
    U = U/np.tile(col_sum,(cluster_n,1))
    return U

def stepfcm(data,data1,center,U,cluster_n,expo,alfa,segma):
#模糊C均值聚类时迭代的一步
# 输入：
#    data - --- nxm矩阵, 表示n个样本, 每个样本具有m的维特征值
#    data1 - --- nxm矩阵, 表示均值或者中值，均值为FCM_S1算法，中值为FCM_S2算法
#    U - --- 隶属度矩阵
#    cluster_n - --- 标量, 表示聚合中心数目, 即类别数
#    expo - --- 隶属度矩阵U的指数
#    alfa - --- punishment factor
# 输出：
#    U_new - --- 迭代计算出的新的隶属度矩阵
#    center - --- 迭代计算出的新的聚类中心
#    obj_fcn - --- 目标函数值

    mf=np.power(U,expo)
    K=Kernel(data,center,segma)
    K1=Kernel(data1,center,segma)

    center=np.sum(mf*(K*(np.outer(np.ones((cluster_n,1)),data.T))+alfa*K1*np.outer(np.ones((cluster_n,1)),data1.T)),axis=1)/np.sum(mf*(K+alfa*K1),axis=1)
    center=center.reshape((-1,1))

    dist=2*(1-K)
    dist1=2*(1-K1)

    obj_fcn=sum(sum(np.power(dist,2)*mf))+alfa*sum(sum(np.power(dist1,2)*mf))  #计算目标函数值
    x=np.power(dist,2)+alfa*np.power(dist1,2)
    if(np.array(np.where(x==0)).size!=0):
        raise Exception('zero')
    else:
        tmp =np.power(x,(-1/(expo-1)))
    U_new = tmp/np.outer(np.ones((cluster_n,1)),sum(tmp))  #计算新的隶属度矩阵
    return  U_new,center,obj_fcn

def estimateSegma(data):
#计算高斯距离的参数
# 输入：
#    data - --- 数据点
# 输出：
#    segma2 - --- 参数σ ^ 2

    mean_data=np.mean(data,axis=0)
    segma2=np.dot((data-mean_data).T,(data-mean_data))/data.size
    return segma2

def Kernel(data,center,segma2):
#计算高斯距离
# 输入：
#    data - --- 数据点
#    center - --- 聚类中心
#    segma2 - --- 参数σ
# 输出：
#    d - --- 高斯距离

    d=np.zeros((center.size,data.size))
    data=data.T
    for k in range(0,center.size):  #对每一个聚类中心
        #每一次循环求得所有样本点到一个聚类中心的距离
        d[k]=np.exp(-np.power((data-center[k]),2)/segma2)
    return d