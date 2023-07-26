import random
import numpy as np
import math
from random import randint
# from scipy import linalg
def scalmul(n,l):
    l1=l.copy()
    for i in range(len(l)):
        l1[i]=l1[i]*n
    return l1
def listadd(l1,l2):
    l3=l1.copy()
    for i in range(len(l1)):
        l3[i]+=l2[i]
    return l3
def rand_unimod(n):
    random_matrix = [[random.randint(-120,120) for _ in range(n) ] for _ in range(n)]
    upperTri = np.triu(random_matrix)
    lowerTri = [[np.random.randint(-120,120) if x<y else 0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            upperTri[i][j]=int(upperTri[i][j])
            lowerTri[i][j]=int(lowerTri[i][j])
    r = 0
    c = 0
    for r in range(len(upperTri)):
        for c in range(len(lowerTri)):
            if r==c:
                if bool(random.getrandbits(1)):
                    upperTri[r][c]=1
                    lowerTri[r][c]=1
                else:
                    upperTri[r][c]=-1
                    lowerTri[r][c]=-1
    uniModular = np.matmul(upperTri,lowerTri)
    for i in range(len(uniModular)):
        for j in range(len(uniModular)):
            uniModular[i][j]=int(uniModular[i][j])
    # print("det: ", np.linalg.det(uniModular))
    # if(np.linalg.det(uniModular) == 1):
    return uniModular
def hadamard_ratio(basis,n):
        detOfLattice = np.linalg.det(basis)
        mult=1
        for v in basis:
            mult = mult * np.linalg.norm(v)
        ratio = (detOfLattice/mult)**(1.0/n)
        return ratio
def encryption(msg,bad_basis,bad_diff,badstart,bad_mod,error_start, error_diff, num):
    coord=[0]*len(bad_basis)
    for i in range(len(bad_basis)):
        for j in range(len(bad_basis)):
            bad_basis[i][j]=int(bad_basis[i][j])
    for i in range(len(bad_basis)):
        rand=random.randint(3,6)
        for j in range(len(bad_basis)):
            coord[j]+=bad_basis[i][j]*rand
    # print("coord",coord)
    n=num
    # for i in range(len(coord)):
    #     n.append(((bad_mod[i]-1 - badstart[i])/bad_diff[i])+1)
    # print("num",n)
    # ciphertext=[]
    points=[]
    # for i in range(26):
        # points.append([])
    for j in range(len(n)):
        temp=[]
        for i in range(26):
            temp.append([])
        for i in range(1,int(n[j]+1)):
            # if i%26==j:
            temp[i%26 -1].append(i)
        points.append(temp)
    # print("points",points)
    zeropoints=[[i for i in range(1,int(n[j]+1)) if i%2!=0] for j in range(len(n))]
    onepoints=[[i for i in range(1,int(n[j]+1)) if i%2==0] for j in range(len(n))]
    # print("zeropoints and one points",zeropoints, onepoints)
    minch=float("inf")
    # print("message",msg)
    for i in range(len(msg)):
        ch=random.choice(points[i][msg[i]])
        if ch<minch:
            minch=ch
        for j in range(ch):
            coord=listadd(listadd(coord,badstart[i]),scalmul(j,bad_diff[i]))
    # for i in range(len(msg)):
    #     if msg[i]==0:
    #         ch=random.choice(zeropoints[i])
    #         if ch<minch:
    #             minch=ch
    #         for j in range(ch):
    #             coord=listadd(listadd(coord,badstart[i]),scalmul(j,bad_diff[i]))
    #     else:
    #         ch=random.choice(onepoints[i])
    #         if ch<minch:
    #             minch=ch
    #         for j in range(ch):
    #             coord=listadd(listadd(coord,badstart[i]),scalmul(j,bad_diff[i]))
    for j in range(len(coord)):
        coord[j]-=random.randint(0,error_start[i]+(minch-1)*error_diff[i])
    for i in range(len(coord)):
        coord[i]=int(coord[i])
    return coord
def decryption(msg,good_basis, good_diff, good_start, good_mod):
    rem=[]
    gb=np.linalg.inv(good_basis)
    # print(gb)
    # print(good_basis)
    s=np.matmul(msg,np.transpose(gb))
    # print(s)
    for i in range(len(s)):
        s[i]=math.floor(s[i])
    # print(s)
    # s=np.matmul(s,good_basis)
    for i in range(len(good_basis)):
        r1=scalmul(s[i],good_basis[i])
        l=[]
        l1=scalmul(np.dot(msg,good_basis[i])/np.dot(good_basis[i],good_basis[i]),(good_basis[i]))
        # print("l1",l1)
        l1=np.transpose(l1)
        for j in range(len(r1)):
            l.append(l1[j]-r1[j])
        rem.append(l)
    # print("rem:",rem)
    for i in range(len(rem)):
        for j in  range(len(rem[i])):
            rem[i][j]=int(rem[i][j])
            # if good_basis[i][j]==0:
                # rem[i][j]=0
    # print(rem)
    # for i in range(len(msg)):
    #     rem.append(msg[i]%good_basis[i][i])
    
    # # print(rem)
    finalmsg=[]
    # for j in range(len(rem)):
    #     for i in range(len(rem)):
    #         temp=0
    #         j=0
    #         while temp<rem[j][i]:
    #             temp+=good_start[j][i]+ j*good_diff[j][i]
    #             # print(temp)
    #             j+=1
    #         finalmsg.append(j)
    for i in range(len(rem)):
        temp=[0]*len(rem)
        j=0
        flag=0
        count=0
        for k in range(len(temp)):
            if temp[k]>=rem[i][k]:
                count+=1
        while flag==0 and count!=len(temp):
            temp2=listadd(good_start[i], scalmul(j,good_diff[i]))
            temp=listadd(temp,temp2)
            j+=1
            count=0
            for k in range(len(temp)):
                if temp2[k]>0:
                    if temp[k]>=rem[i][k]:
                        count+=1
                else:
                    if temp[k]<=rem[i][k]:
                        count+=1
            if count==len(temp):
                flag=1
        finalmsg.append(j)
    # 
    for i in range(len(finalmsg)):
        # if finalmsg[i]%2==0:
        #     finalmsg[i]=1
        # else:
        #     finalmsg[i]=0
        # if finalmsg[i]%26==2:
        #     finalmsg[i]=1
        # elif finalmsg[i]%26==1:
        #     finalmsg[i]=0
        if finalmsg[i]%26!=0:
            finalmsg[i]=finalmsg[i]%26 -1 
        else:
            finalmsg[i]=25
    # print("finalmsg:", finalmsg)
    return finalmsg

n = int(input("Enter n: "))
# result = genmat(n)
badstart=[]
good_start=[]
good_diff=[]
bad_diff=[]
message=[]
# num=
num=[]
for i in range(n):
    num.append(26*random.randint(10,50))
for i in range(n):
    message.append(random.randint(0,25))
    l=[]
    l1=[]
    for j in range(n):
        if i==j:
            l.append(random.randint(5,20))
            l1.append(random.randint(5,20))
        else:
            l.append(0)
            l1.append(0)
    good_start.append(l)
    good_diff.append(l1)
# print("hi good diff", good_diff)
period=[]
for i in range(len(good_diff)):
    period.append(scalmul(num[i]*0.5,listadd(scalmul(2,good_start[i]) , scalmul((num[i]-1),good_diff[i]))))
for i in range(n):
    list1=[0]*n
    for j in range(n):
        list1=listadd(list1,scalmul(random.randint(1,3),period[j]))
    # badstart.append(listadd(list1, good_start[i]))
    bad_diff.append(listadd(good_diff[i],list1))
for i in range(n):
    list1=[0]*n
    for j in range(n):
        list1=listadd(list1,scalmul(random.randint(1, 3),period[j]))
    badstart.append(listadd(list1, good_start[i]))
# print(badstart)
good_mod=[]
bad_mod=[]
for i in range(len(good_diff)):
    good_mod.append(listadd(scalmul((num[i]-1),good_diff[i]) , good_start[i]))
for i in range(len(good_diff)):
    for j in range(len(good_mod)):
        good_mod[i][j]+=1
for i in range(len(bad_diff)):
    bad_mod.append(listadd(scalmul((num[i]-1),bad_diff[i]) , badstart[i]))
for i in range(len(good_diff)):
    for j in range(len(bad_mod)):
        bad_mod[i][j]+=1
# print("badstart",badstart)
# print("good start",good_start)
# print("good_diff",good_diff)
# print("bad_diff",bad_diff)
# print("period",period)
# print("num",num)
# print(good_mod,bad_mod)
# print(40%22)
good_basis=period.copy()
# for i in range(n):
#     good_basis.append([0]*n)
# for i in range(n):
#     good_basis[i][i]=period[i]
# i=0
# print("good basis",good_basis)
bad_basis=[]
while True:
        bad_vector = rand_unimod(n)
        temp=np.matmul(good_basis,bad_vector)
        ratio = hadamard_ratio(temp,n)
        # print("ratio = ",ratio)
        # if i<n-1:
        #     print("cos = ",np.dot(temp[i],temp[i+1])/(np.linalg.norm(temp[i])*np.linalg.norm(temp[i+1])))
        # i+=1
        # bad_basis=temp
        # break
        if ratio <= 0.1 or math.isnan(ratio) :
            bad_basis=temp	
            break
# print("bad_basis",bad_basis)
error_start=[]
error_diff=[]
message=[]
for i in range(n):
    percentage=random.randint(10,40)
    percentage2=random.randint(10,40) 
    l=[]
    l2=[]
    m=scalmul((percentage/100),good_start[i])
    o=scalmul((percentage2/100),good_diff[i])
    for j in range(len(m)):
        m[j]=int(m[j])
        o[j]=int(o[j])
    for j in range(n):
        l.append(m[j])
        l2.append(o[j])
    error_start.append(l)
    error_diff.append(l2)
    # error_start.append(random.randint([0]*n,scalmul((percentage/100),good_start[i])))
    # error_diff.append(random.randint([0]*n,int(percentage2*good_diff[i]/100)))
for i in range(1,n):
    error_start[0]=listadd(error_start[0],error_start[i])
    error_diff[0]=listadd(error_diff[0],error_diff[i])
error_start=error_start[0]
error_diff=error_diff[0]
print("error_start",error_start)
print("errordiff",error_diff)
# for l in range(10):
message=[]
# print("error_start, error diff",error_start, error_diff)
# print("message",message)
# good_basis=[[1,0],[0,1]]
# bad_basis=np.matmul([[4,5],[5,6]], good_basis)
bad_basis=np.transpose(bad_basis)
print("bad_basis",bad_basis)
# print(error_start, error_diff)
for jk in range(5):
    message=[]
    for i in range(n):
        message.append(random.randint(0,25))
    ciphertext=encryption(message, bad_basis,bad_diff,badstart,bad_mod,error_start, error_diff, num)
    print("ciphertext:",ciphertext)
    print("-------------------MSG---------------")
    print(message)
    print("--------------Decryption-------------")
    msg=decryption(ciphertext, good_basis,good_diff, good_start, good_mod)
    print(msg)
    print(message==msg)
    l1=[]
    for i in range(len(msg)):
        if msg[i]!=message[i]:
            print(" ",i)