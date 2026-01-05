n=int(input("请输入自然数n:"))
sum=1             
if n%2==1:     
  for i in range(3, n+1,2):
      sum=sum+1/i**2
else:
                #补充偶数部分的代码
 
print(round(sum,4))





