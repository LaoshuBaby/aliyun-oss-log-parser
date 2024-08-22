import os
import time

start_time=time.time()
total=len(os.listdir())
print(total)
log_data=[]

lst_file=[]

count=0
for i in os.listdir():
    if count<10:
        lst_file.append(i)
        print(f"[{count+1}/{total}] {i}")
        count+=1


for i in lst_file:
    with open(i,"r",encoding="UTF-8") as f:
        tmp_data=f.read().split("\n")
        for i in tmp_data:
            log_data.append(i)

print(len(log_data))

with open("p.log","w",encoding="utf-8") as f:
    f.write("\n".join(log_data))

end_time=time.time()
use_time=end_time-start_time
print(f"use {use_time}s")

请你优化这段代码

1. 全都用wrapper来对函数计时，提供一个main函数
2. 优化变量名令其更规则，更有规律，更易懂
3. 无需使用try-exception