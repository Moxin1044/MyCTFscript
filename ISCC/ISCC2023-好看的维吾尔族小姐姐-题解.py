import cv2
import pylibdmtx.pylibdmtx as dmtx
from html.parser import HTMLParser
import html

img = cv2.imread("timu.png")

flipped_img = cv2.flip(img, 1)  # 翻转图片

cv2.imwrite("1.png", flipped_img)

img = cv2.imread("1.png")  # 识别码

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
decoded_objects = dmtx.decode(gray)
flags = ""
for obj in decoded_objects:
    flags += obj.data.decode()

flag=flags[::-1]
print(html.unescape(flag))  # 解HTML实体编码

