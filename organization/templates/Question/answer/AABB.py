for i in range(34,100):
  n=i**2
  a=n//1000
  b=n//100%10
  c=n%100//10
  d=n%10
  if a==b and c==d and n>1000: 
    print("输出这个四位数：",n)
