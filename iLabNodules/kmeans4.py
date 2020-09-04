import numpy as np
def kmeans4(I):
    k=4
    m,n=I.shape
    X=np.reshape(I,(-1,1),'F')
    X=X.astype(np.float64)
    A=X
    A=np.compress(np.all(A!=0,axis=1),A).reshape((-1,1))
    a,b=A.shape
    np.random.seed(0)
    C=A[np.random.choice(np.arange(a*b),k,False),:]
    J_prev=float('inf')
    iter=0
    tol=1e-2
    while True :
        iter=iter+1
        dist=(np.sum(np.power(X,2),axis=1)*np.ones((k,1))).T+np.sum(np.power(C,2),axis=1)*np.ones((m*n,1))-2*np.matmul(X,C.T)
        label=dist.argmin(axis=1)
        for i in range(0,k):
            C[i]=np.mean(X[label==i,:],axis=0)
        J_cur=np.sum(np.power(X-C[label,:],2))
        if abs(J_cur-J_prev)<tol:
            break
        J_prev=J_cur
    C=np.sort(C.flatten()).reshape((-1,1))
    return C
