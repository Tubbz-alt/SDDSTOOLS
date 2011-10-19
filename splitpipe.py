#!/usr/bin/env python
from subprocess import *
import shutil
import os
import shlex

inSub=Popen(shlex.split('cat in.txt'),stdout=PIPE)
print inSub.poll()

queue=[]
for i in range(0,3):
	temp=Popen(['cat'],stdin=PIPE)
	queue=queue+[temp]

while True:
	# print 'hi'
	buf=os.read(inSub.stdout.fileno(),10000)
	if buf == '': break
	for proc in queue:
		proc.stdin.write(buf)
for proc in queue:
    proc.stdin.close()

# queue[1].communicate()
queue[0].wait()
print queue[0].poll()
