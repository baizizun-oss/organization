#居民年度水费计算程序
yuefen=["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月","合计"]  #月份列表
yongshuiliang=[9,15,7,6,9,12,22,25,13,8,9,5,0]  #用水量列表
shuifei=[0,0,0,0,0,0,0,0,0,0,0,0,0]  #水费列表
zongbiao=[yuefen,yongshuiliang,shuifei]  #总表

#显示水费详单的原始表
j=0
print("\t","年度居民水费详单(原始表)")
print("月份","\t\t","用水量","\t\t","水费")
while j<13:
    print(yuefen[j],"\t\t",yongshuiliang[j],"\t\t",shuifei[j])
    j=j+1
print()
print()
#根据每月用水量计算每月水费
i=0
yslsum=0
sfsum=0
while i<12:
    
#在以下区域继续完善代码












    
    i=i+1
else:
    yongshuiliang[12]=yslsum
    shuifei[12]=sfsum
    
#显示处理后水费详表
j=0
print("\t","年度居民水费详单（处理后表）")
print("月份","\t\t","用水量","\t\t","水费")
while j<13:
    print(yuefen[j],"\t\t",yongshuiliang[j],"\t\t",shuifei[j])
    j=j+1
#程序结束
