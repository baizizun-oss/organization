#删除标号，并在标号的位置补充代码
n=int(input("请输入1个整数作为密钥："))  
mingw=<1>("请输入明文文本：")
b=""
for p in mingw:
     if 'a'<=p<='z':#对小写字符进行加密
         b=b+chr(ord('a')+(ord(p)-ord('a')+n)%26) 
     elif 'A'<=p<='Z':#对大写字符进行加密
         b=<2>  
     else:
         b=b+p
print(<3>)  #输出加密后的文本 ‘9’
