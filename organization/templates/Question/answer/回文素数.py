def prime(n):   #该函数用来判断n是否为素数
    for i in range(2,int(n**0.5)+1):
        if n%i==0  :
            return False
    return True             

def rev(n):  #该函数用来得出n的反读数
    t=0
    while n>0:  #将以下程序补充完整
      
    return t
for i in range(100,1001): #输出100—1000内的所有回文素数
    if rev(i)==i and prime(i)    :
            print(i,end=" ")
    


