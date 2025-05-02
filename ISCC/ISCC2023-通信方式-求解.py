from scipy.io import wavfile
import numpy as np
from PIL import Image
import math
sample_rate, data = wavfile.read('telegram2wechat.wav')
left_channel = data[:, 0]
right_channel = data[:, 1]
result = left_channel - right_channel
np.savetxt('array.txt',result,fmt='%d')
with open('array.txt', 'r') as file:
    file_contents = file.readlines()
file_contents = [int(line.strip()) for line in file_contents]
flag = [x for x in file_contents if x != 0]
flag_new = ""
for t in flag:
    flag_new += str(t)
flag_new = flag_new.replace("2", "0")
print(flag_new)
print(len(flag_new))
MAX = int(math.sqrt(len(flag_new)))
print(MAX)
pic = Image.new("RGB",(MAX,MAX))
i=0
for y in range(0,MAX):
    for x in range(0,MAX):
        if(flag_new[i] == '1'):
            pic.putpixel([x,y],(0,0,0))
        else:pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("\flag.png")