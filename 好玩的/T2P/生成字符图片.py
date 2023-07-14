from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 字体文件路径
font_path = 'font/simsun.ttc'
# 设置字体和字号
font_size = 64
font = ImageFont.truetype(font_path, size=font_size)
# 设置画布大小


def draw_char(char):
    # 创建画布和画笔
    im = Image.new('RGB', canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(im)

    # 在画布中心写字
    bbox = draw.textbbox((0, 0), char, font=font)
    x = (canvas_size[0] - bbox[2] - bbox[0]) // 2 - bbox[0]
    y = (canvas_size[1] - bbox[3] - bbox[1]) // 2 - bbox[1] + 5
    draw.text((x, y), char, font=font, fill=(0, 0, 0))

    # 转换成numpy数组
    im_arr = np.array(im)
    return Image.fromarray(im_arr)


if __name__ == '__main__':
    text = input('请输入文本：')
    canvas_size = (len(text)*font_size, font_size)
    char_im = draw_char(text)
    char_im.save(f'output/T2P.png')