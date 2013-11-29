# encoding=utf-8
import os
import re


output = os.popen('netstat -aon|findstr ":"8081').readlines()
for i in output:
    #print(i.strip().split('       '))
    print(re.split('\s+', i.strip())[4])
