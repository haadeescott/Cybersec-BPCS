import sys
import cv2 
import numpy as np
import random

def extract():
    J=cv2.imread('mhw2_stego.png') # insert stengo object 
    f= open('output_payload.txt', 'w+', errors="ignore")

    idx=0
    bitidx=0
    bitval=0
    decoded_data = ""

    for i in range(J.shape[0]):
        if (I[i, 0, 0]== '-'):
            break 
        for j in range(J.shape[1]):
            for k in range(3):
                if (I[i, j, k]== '-'):
                    break
                if bitidx==8:
                    if bitval in list(all_asci_data):
                        f.write(chr(bitval))
                        bitidx=0
                        bitval=0
                bitval |= (I[i, j, k]%2)<<bitidx
                bitidx+=1
    
    f.write(decoded_data)
    f.close()

bits = []
f=open('payload.txt', 'r')
# uses ASCII value system
blist = [ord(b) for b in f.read()]
all_asci_data = []
for b in blist:
    all_asci_data.append(b)
    for i in range(8):
        bits.append((b>>i) & 1)

I = np.asarray(cv2.imread('mhw2.jpg')) # insert original picture

sign = [1, -1]
idx=0
print(I.shape)
for i in range(I.shape[0]):
    for j in range(I.shape[1]): 
        for k in range(3):
            if idx<len(bits):
                if I[i][j][k]%2 != bits[idx]:
                    s=sign[random.randint(0,1)]
                    if I[i][j][k]==0: s=1
                    if I[i][j][k]==255:s=-1
                    I[i][j][k]+=s
                idx+=1

cv2.imwrite('mhw2_stego.png', I)

print("Extracting . . .")
extract()
print("Completed")