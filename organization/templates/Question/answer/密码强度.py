n=0
while n<8:
    password=input("请输入要检测的密码：")
    n=len(password)  #len用来获取字符串长度
    if n<8:
        print("密码位数不能少于8位，请重新输入！")
    
n1=0
n2=0
n3=0
for i in range(0,n):
    ch= password[i]
    if "0"<=ch<="9":
        n1=1
    elif "a"<=ch<="z" or "A"<=ch<="Z":
        n2=1
    else:
        n3=1
x=n1+n2+n3
#根据流程图补充下面程序
if x==3:
    print("强")
elif x==2:
    print("中")
else:
    print("弱")








#程序结束   

