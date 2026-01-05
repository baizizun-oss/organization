def fib(x): 
    if(x == 1 or x == 2): 
        return 1 #返回第1,2项
    a = 1; b = 1; i = 3
    while(i <= x):
        temp = a
        a = b
        b = temp+a
        i = i + 1
    return b #返回第x项

n = int(input("请输入一个正整数n：")) #自键盘接收正整数n
for i in range(1,n+1):
    print(fib(i), end = ' ') #输出一个n项的斐波那契数列
