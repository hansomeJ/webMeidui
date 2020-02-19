import time
import re

# print(t1)
s=re.findall('\d+', '3.15V')
m=s[0]+'.'+s[1]
print(m>'2')